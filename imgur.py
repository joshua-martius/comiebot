from discord import utils
import discord
import random
import string
import urllib.request
from PIL import Image

imageIDs = []
authorIDs = []
votes = []

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

        votes[index] = votes[index] + 1
        return