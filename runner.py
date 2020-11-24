import comie
import json
import discord

config = json.loads(open("./config.json","r").read())

intents = discord.Intents.default()
intents.members = True
bot = comie.Comie(intents=intents)
bot.run(config["discord"]["token"])