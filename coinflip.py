from discord import utils
import discord
import random

class coinflip():

    async def flip(message):
        rnd = random.randint(0,1)
        if rnd == 0:
            await message.channel.send('Kopf!👤')
        else:
            await message.channel.send('Zahl!1️⃣')
        return