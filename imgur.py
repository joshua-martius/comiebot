from discord import utils
import discord
import random
import string
import urllib.request
from PIL import Image

imageIDs = []
authorIDs = []
votes = []
images = []

def mentionUser(user):
    return "<@" + str(user.id) + ">"

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

        imageIDs.append(message.id)
        authorIDs.append(author.id)
        votes.append(0)
        return

    async def postResults(self, channel):
        winnerIndex = votes.index(max(votes))
        return [imageIDs[winnerIndex], votes[winnerIndex], authorIDs[winnerIndex]]


    ## ToDo: clean up this mess
    async def reaction(self, reaction, user, removal):
        imgid = reaction.message.id
        index = imageIDs.index(imgid)

        if reaction.emoji == "👀":
            if removal:
                votes[index] = votes[index] + 1
                return
            votes[index] = votes[index] - 1
            if votes[index] <= -3:
                author = await self.fetch_user(authorIDs[index])
                await reaction.message.delete() # delete image with a score of -3 or lower
                await reaction.message.channel.send("Ich habe ein Bild von %s verschwinden lassen! 🤭" % (mentionUser(author)))
        else:
            if removal:
                votes[index] = votes[index] - 1
                if votes[index] <= -3:
                    author = await self.fetch_user(authorIDs[index])
                    await reaction.message.delete() # delete image with a score of -3 or lower
                    await reaction.message.channel.send("Ich habe ein Bild von %s verschwinden lassen! 🤭" % (mentionUser(author)))
                return
            
            votes[index] = votes[index] + 1
        return