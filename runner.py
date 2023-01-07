import comie
import json
import discord
from configwrapper import configwrapper

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = comie.Comie(intents=intents)
bot.run(configwrapper.getEntry("DISCORD_TOKEN"))