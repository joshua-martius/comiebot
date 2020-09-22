import discord
import random
from discord import utils
from secretsanta import secretsanta
from imgur import imgur

adminNames = ["y0sh1#1990", "Sh4ky#3017"]

def mentionUser(user):
    return "<@" + str(user.id) + ">"

class Comie(discord.Client):
    santaRoleName = "Wichtel"

    ### REACIONS
    async def on_reaction_add(self, reaction, user):
        if str(reaction.message.author) != "Comie#1396":
            return
        if reaction.emoji != "👍" and reaction.emoji != "👀":
            return
        
        await imgur.reaction(self, reaction, user)
        return


    ### READY MESSAGE
    async def on_ready(self):
        print("Bot is up and running.")
        return
    
    async def on_message(self, message):
        if message.author == self.user: 
            return

        message.content = str(message.content).lower()

        ##### SECRET SANTA
        if message.content.startswith("!wichteln") and str(message.author) in adminNames:
            await secretsanta.exec(self, message)
            return

        ##### IMGUR
        elif message.content.startswith("!img"):
            await message.channel.send("Hier kommt ein zufälliges Bild für dich %s ~(^__^)~" % (mentionUser(message.author)))
            await imgur.postImage(self, message, message.author)
            return

        elif message.content.startswith("!results"):
            results = await imgur.postResults(self, message.channel)
            winmsg = await message.channel.fetch_message(results[0])
            winner = await self.fetch_user(results[2])
            
            await message.channel.send("Gewonnen hat %s mit %d Votes für das gepinnte Bild!" % (mentionUser(winner), int(results[1])))
            await winmsg.pin()
            return
        
        ##### SELF HELP
        elif message.content.startswith("!help"):
            await message.channel.send("Hi " + mentionUser(message.author) + "!\nIch kann folgende Befehle bearbeiten:\n!help - Zeigt diese Hilfe an\n!img - Schickt ein zufälliges Bild in den aktuellen Channel (Upvote: 👍 | Downvote: 👀)\n!wichteln - Startet eine Wichtelpaar Auslosung")
            return

        ##### UNKNOWN COMMAND
        elif message.content.startswith("!") and len(message.content) != 0:
            await message.channel.send("Den Befehl kenne ich nicht :/")
            return