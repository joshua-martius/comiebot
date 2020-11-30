from discord import utils
import discord
import random
import string
import urllib.request
from PIL import Image
import mysql.connector
import json

config = json.loads(open("./config.json","r").read())

images = []

def mentionUser(user):
    return "<@" + str(user.id) + ">"

mydb = mysql.connector.connect(
  host=config["db"]["host"],
  user=config["db"]["user"],
  password=config["db"]["password"],
  database=config["db"]["name"]
)


sql = mydb.cursor()

def executeSql(cmd):
    mydb.connect()
    print("Executing: " + cmd)
    if cmd.startswith("SELECT"):
        sql.execute(cmd)
        result = sql.fetchall()
        mydb.close()
        return result
    else:
        # insert, update or delete
        sql.execute(cmd)
        mydb.commit()
        mydb.close()
        return

class imgur():

    async def postImage(self, message, author):
        baseString = "https://i.imgur.com"
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        ### generate unique id
        tries = 0
        while True:
            length = random.randint(5,6)
            tries = tries + 1
            if tries >= 100:
                await message.channel.send("Ich habe nach %d Versuchen kein neues Bild finden können </3" % (tries))
                return
            id = ''.join(random.choice(chars) for i in range(length))
            if id in images:
                continue
            url = "%s/%s.png" % (baseString, id)
            
            try:
                urllib.request.urlretrieve(url, './img.png')
                with Image.open("img.png") as img:
                    if img.width != 161 and img.height != 81: # in case of the imgur error image
                        break
            except:
                continue
        ### when unique id was found
        images.append(id)

        message = await message.channel.send(file=discord.File('img.png'))

        # add image to voting table
        cmd = "INSERT INTO tblVoting(vMessage, vAuthor) VALUES ('%s','%s')" % (message.id, author.id)
        executeSql(cmd)
        return

    async def postResults(self, channel):
        cmd = "SELECT vMessage,vVotes,vAuthor FROM tblVoting WHERE vVotes = (SELECT MAX(vVotes) FROM tblVoting) LIMIT 1"
        result = executeSql(cmd)
        return [result[0][0],result[0][1], result[0][2]]

    ## ToDo: clean up this mess
    async def reaction(self, payload, channel, removal):
        imgid = payload.message_id

        if payload.emoji.name == "👀":
            if removal:
                cmd = "UPDATE tblVoting SET vVotes = vVotes + 1 WHERE vMessage = '%s'" % (imgid)
                executeSql(cmd)
                return
            cmd = "UPDATE tblVoting SET vVotes = vVotes - 1 WHERE vMessage = '%s'" % (imgid)
            executeSql(cmd)
            cmd = "SELECT vVotes,vAuthor FROM tblVoting WHERE vMessage = '%s'" % (imgid)
            result = executeSql(cmd)
            if int(result[0][0]) <= -3:
                author = await self.fetch_user(result[0][1])
                #message = await self.fetch_message(imgid)
                await self.http.delete_message(payload.channel_id, payload.message_id) # delete image with a score of -3 or lower!
                await channel.send("Ich habe ein Bild von %s verschwinden lassen! 🤭" % (mentionUser(author)))
                cmd = "DELETE FROM tblVoting WHERE vMessage = '%s'" % (payload.message_id)
                executeSql(cmd)
        else:
            if removal:
                cmd = "UPDATE tblVoting SET vVotes = vVotes - 1 WHERE vMessage = '%s'" % (imgid)
                executeSql(cmd)
                cmd = "SELECT vVotes,vAuthor FROM tblVoting WHERE vMessage = '%s'" % (payload.message_id)
                result = executeSql(cmd)
                if int(result[0][0]) <= -3:
                    author = await self.fetch_user(result[0][1])
                    await self.http.delete_message(payload.channel_id, payload.message_id) # delete image with a score of -3 or lower
                    await channel.send("Ich habe ein Bild von %s verschwinden lassen! 🤭" % (mentionUser(author)))
                    cmd = "DELETE FROM tblVoting WHERE vMessage = '%s'" % (payload.message_id)
                    executeSql(cmd)
                return
            
            cmd = "UPDATE tblVoting SET vVotes = vVotes + 1 WHERE vMessage = '%s'" % (imgid)
            executeSql(cmd)
        return