from discord import utils
import discord
import random
import string
import urllib.request
from PIL import Image
import mysql.connector

imageIDs = []
authorIDs = []
votes = []
images = []

def mentionUser(user):
    return "<@" + str(user.id) + ">"

mydb = mysql.connector.connect(
  host="dev.serwm.com",
  user="root",
  password="0c12d1db0cd4edabc8782532d507438d",
  database="comiebot"
)

sql = mydb.cursor()

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
        sql.execute(cmd)
        mydb.commit()
        return

    async def postResults(self, channel):
        cmd = "SELECT vMessage,vVotes,vAuthor FROM tblVoting WHERE vVotes = MAX(vVotes) ORDER BY vCreated DESC LIMIT 1"
        sql.execute(cmd)
        result = sql.fetchone()
        return [result[0],result[1], result[2]]

    ## ToDo: clean up this mess
    async def reaction(self, reaction, user, removal):
        imgid = reaction.message.id

        if reaction.emoji == "👀":
            if removal:
                cmd = "UPDATE tblVoting SET vVotes = vVotes + 1 WHERE vMessage = '%s'" % (imgid)
                sql.execute(cmd)
                mydb.commit()
                return
            cmd = "UPDATE tblVoting SET vVotes = vVotes - 1 WHERE vMessage = '%s'" % (imgid)
            sql.execute(cmd)
            mydb.commit()
            cmd = "SELECT vVotes,vAuthor FROM tblVoting WHERE vMessage = '%s'" % (imgid)
            sql.execute(cmd)
            result = sql.fetchone()
            if int(result[0]) <= -3:
                author = await self.fetch_user(result[1])
                await reaction.message.delete() # delete image with a score of -3 or lower
                await reaction.message.channel.send("Ich habe ein Bild von %s verschwinden lassen! 🤭" % (mentionUser(author)))
        else:
            if removal:
                cmd = "UPDATE tblVoting SET vVotes = vVotes - 1 WHERE vMessage = '%s'" % (imgid)
                sql.execute(cmd)
                mydb.commit()
                cmd = "SELECT vVotes,vAuthor FROM tblVoting WHERE vMessage = '%s'" % (reaction.message.id)
                sql.execute(cmd)
                result = sql.fetchone()
                if int(result[0]) <= -3:
                    author = await self.fetch_user(result[1])
                    await reaction.message.delete() # delete image with a score of -3 or lower
                    await reaction.message.channel.send("Ich habe ein Bild von %s verschwinden lassen! 🤭" % (mentionUser(author)))
                return
            
            cmd = "UPDATE tblVoting SET vVotes = vVotes + 1 WHERE vMessage = '%s'" % (imgid)
            sql.execute(cmd)
            mydb.commit()
        return