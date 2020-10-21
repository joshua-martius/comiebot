import discord
import random
from discord import utils
from secretsanta import secretsanta
from imgur import imgur
from joker import joker
from git import git
import mysql.connector
import time

adminNames = ["y0sh1#1990", "Sh4ky#3017"]

dbcred = []
try:
    with open("./.dbcred") as file:
        for i in range(4):
            line = file.readline()
            dbcred.append(line.strip('\n'))
except:
    print("Couldnt find database credentials in .dbcred file. Exiting.")
    exit()

#mydb = mysql.connector.connect(
#  host=dbcred[0],
#  user=dbcred[1],
#  password=dbcred[2],
#  database=dbcred[3]
#)

#sql = mydb.cursor()

def mentionUser(user):
    return "<@" + str(user.id) + ">"

class Comie(discord.Client):
    santaRoleName = "Wichtel"

    ### REACIONS
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name != "👍" and payload.emoji.name != "👀":
            return
        
        channel = await self.fetch_channel(payload.channel_id)

        await imgur.reaction(self, payload, channel, False)
        return

    async def on_raw_reaction_remove(self, payload):
        if payload.emoji.name != "👍" and payload.emoji.name != "👀":
            return
        
        channel = await self.fetch_channel(payload.channel_id)

        await imgur.reaction(self, payload, channel, True)
        return

    ### READY MESSAGE
    async def on_ready(self):
        print("Bot is up and running.")
        return
    
    async def on_message(self, message):
        if message.author == self.user: 
            return
        
        if not message.content.startswith("!"):
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

            ### hue color flip
            #sql.execute("INSERT INTO tblHue(cCommand,cAuthor,cDone) VALUES ('Wohnzimmerlampe,on,True','%s',0)" % (str(message.author)))
            #time.sleep(0.5)
            #sql.execute("INSERT INTO tblHue(cCommand,cAuthor,cDone) VALUES ('Wohnzimmerlampe,on,False','%s',0)" % (str(message.author)))
            #time.sleep(0.5)
            #sql.execute("INSERT INTO tblHue(cCommand,cAuthor,cDone) VALUES ('Wohnzimmerlampe,on,True','%s',0)" % (str(message.author)))
            #time.sleep(0.5)
            #sql.execute("INSERT INTO tblHue(cCommand,cAuthor,cDone) VALUES ('Wohnzimmerlampe,on,False','%s',0)" % (str(message.author)))
            #mydb.commit()

            return

        elif message.content.startswith("!results") and str(message.author) in adminNames:
            results = await imgur.postResults(self, message.channel)
            winmsg = await message.channel.fetch_message(results[0])
            winner = await self.fetch_user(results[2])
            
            await message.channel.send("Gewonnen hat %s mit %d Votes für das gepinnte Bild!" % (mentionUser(winner), int(results[1])))
            await winmsg.pin()
            return
        
        #### JOKE
        elif message.content.startswith("!joke"):
            await joker.exec(self, message)
            return

        #### GITHUB BUGS
        elif message.content.startswith("!bugs"):
            await message.channel.send(git.exec(self))
            return

        #elif message.content.startswith("!light"):
        #    params = message.content.split(" ")[1:]
        #    cmd = params[0].lower()
        #    if cmd == "on":
        #        sql.execute("INSERT INTO tblHue(cCommand,cAuthor,cDone) VALUES ('Wohnzimmerlampe,on,True','%s',0)" % (str(message.author)))
        #        await message.channel.send("Ich mach dann mal das Licht an!")
        #    elif cmd == "off":
        #        sql.execute("INSERT INTO tblHue(cCommand,cAuthor,cDone) VALUES ('Wohnzimmerlampe,on,False','%s',0)" % (str(message.author)))
        #        await message.channel.send("Ich mach dann mal das Licht aus!")
        #    elif cmd == "color":
        #        if not params[1].isnumeric():
        #            return
        #        val = int(params[1])
        #        sql.execute("INSERT INTO tblHue(cCommand,cAuthor,cDone) VALUES ('Wohnzimmerlampe,hue,%d','%s',0)" % (val,str(message.author)))
        #        await message.channel.send("Ich mach dann mal das Licht farbig!")
        #    else:
        #        return
        #    mydb.commit()
        #    return

        ##### SELF HELP
        elif message.content.startswith("!help"):
            await message.channel.send("Hi " + mentionUser(message.author) + "!\nIch kann folgende Befehle bearbeiten:\n!help - Zeigt diese Hilfe an\n!img - Schickt ein zufälliges Bild in den aktuellen Channel (Upvote: 👍 | Downvote: 👀)\n!wichteln - Startet eine Wichtelpaar Auslosung\n!joke - Erzählt einen Witz\n!bugs - Gibt alle bekannten Fehler aus")
            return

        ##### UNKNOWN COMMAND
        elif len(message.content) != 0:
            await message.channel.send("Den Befehl kenne ich nicht :/")
            return
