from discord import utils
import discord
import string
import urllib.request, json 
from asyncio import sleep

jokeIDs = []

class joker():

    async def exec(self, message):
        with urllib.request.urlopen("https://official-joke-api.appspot.com/random_joke") as url:
            data = json.loads(url.read().decode())
            if data["id"] in jokeIDs:
                await joker.exec(self, message)
                return
            else:
                jokeIDs.append(data["id"])
                await message.channel.send(data["setup"])
                await sleep(3)
                await message.channel.send(data["punchline"])
        return