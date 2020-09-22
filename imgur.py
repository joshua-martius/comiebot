from discord import utils
import discord
import random
import string
import urllib.request
from PIL import Image

imageIDs = []
authorIDs = []
votes = []

def mentionUser(user):
    return "<@" + str(user.id) + ">"

class imgur():

    async def postImage(self, message, author):
        baseString = "https://i.imgur.com"
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        len = random.randint(5,6)
        id = ''.join(random.choice(chars) for i in range(5))
        url = "%s/%s.png" % (baseString, id)
        
        urllib.request.urlretrieve(url, './img.png')

        with Image.open("img.png") as img:
            if img.width == 161 and img.height == 81: # in case of the imgur error image
                await imgur.postImage(self, message, author)
                return

        message = await message.channel.send(file=discord.File('img.png'))

        imageIDs.append(message.id)
        authorIDs.append(author.id)
        votes.append(0)
        return

    async def postResults(self, channel):
        winnerIndex = votes.index(max(votes))
        return [imageIDs[winnerIndex], votes[winnerIndex], authorIDs[winnerIndex]]

    async def reaction(self, reaction, user):
        imgid = reaction.message.id
        index = imageIDs.index(imgid)

        if reaction.emoji == "👀":
            votes[index] = votes[index] - 1
            if votes[index] <= -3:
                author = await self.fetch_user(authorIDs[index])
                await reaction.message.delete() # delete image with a score of -3 or lower
                await reaction.message.channel.send("Ich habe ein Bild von %s verschwinden lassen! 🤭" % (mentionUser(author)))
        else:
            votes[index] = votes[index] + 1
        return