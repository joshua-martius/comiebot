from discord import utils
import discord
import random
import string
import urllib.request
from PIL import Image

class imgur():    
    async def exec(self, message):
        baseString = "https://i.imgur.com"
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        id = ''.join(random.choice(chars) for i in range(5))
        url = "%s/%s.png" % (baseString, id)
        
        urllib.request.urlretrieve(url, './img.png')

        with Image.open("img.png") as img:
            if img.width == 161 and img.height == 81: # in case of the imgur error image
                await imgur.exec(self, message)
                return

        await message.channel.send(file=discord.File('img.png'))
        return
