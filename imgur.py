from discord import utils
import discord
import random
import string
import urllib.request
from PIL import Image
import mysql.connector

images = []

def mentionUser(user):
    return "<@" + str(user.id) + ">"

dbcred = []
try:
    with open("./.dbcred") as file:
        for i in range(4):
            line = file.readline()
            dbcred.append(line.strip('\n'))
except:
    print("Couldnt find database credentials in .dbcred file. Exiting.")
    exit()

mydb = mysql.connector.connect(
  host=dbcred[0],
  user=dbcred[1],
  password=dbcred[2],
  database=dbcred[3]
)


sql = mydb.cursor()

def executeSql(cmd):
    print("Trying to execute: " + cmd)
    if cmd.startswith("SELECT"):
        sql.execute(cmd)
        result = sql.fetchall()
        return result
    else:
        # insert, update or delete
        sql.execute(cmd)
        mydb.commit()
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
            url = "%s/%s.png" % (baseString, id)
            
            try:
                urllib.request.urlretrieve(url, './img.png')
                with Image.open("img.png") as img:
                    if img.width != 161 and img.height != 81 and id not in images: # in case of the imgur error image
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
    async def reaction(self, reaction, user, removal):
        imgid = reaction.message.id

        if reaction.emoji == "👀":
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
                await reaction.message.delete() # delete image with a score of -3 or lower
                await reaction.message.channel.send("Ich habe ein Bild von %s verschwinden lassen! 🤭" % (mentionUser(author)))
        else:
            if removal:
                cmd = "UPDATE tblVoting SET vVotes = vVotes - 1 WHERE vMessage = '%s'" % (imgid)
                executeSql(cmd)
                cmd = "SELECT vVotes,vAuthor FROM tblVoting WHERE vMessage = '%s'" % (reaction.message.id)
                result = executeSql(cmd)
                if int(result[0][0]) <= -3:
                    author = await self.fetch_user(result[0][1])
                    await reaction.message.delete() # delete image with a score of -3 or lower
                    await reaction.message.channel.send("Ich habe ein Bild von %s verschwinden lassen! 🤭" % (mentionUser(author)))
                return
            
            cmd = "UPDATE tblVoting SET vVotes = vVotes + 1 WHERE vMessage = '%s'" % (imgid)
            executeSql(cmd)
        return