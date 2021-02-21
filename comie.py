import discord
import random
from discord import utils
from secretsanta import secretsanta
from imgur import imgur
from joker import joker
from coinflip import coinflip
from git import git
from roulette import roulette
from dice import dice
import mysql.connector
import time
import json
from datetime import datetime
from csdating import csdating
from weebnation import weebnation
import requests

config = json.loads(open("./config.json","r").read())

mydb = mysql.connector.connect(
  host=config["db"]["host"],
  user=config["db"]["user"],
  password=config["db"]["password"],
  database=config["db"]["name"]
)

sql = mydb.cursor()

def executeSql(cmd):
    mydb.connect()
    print("Executing: " + cmd)
    if cmd.startswith("SELECT"):
        sql.execute(cmd)
        result = sql.fetchall()
        mydb.close()
        return result
    else:
        # insert, update or delete
        sql.execute(cmd)
        mydb.commit()
        mydb.close()
        return

def mentionUser(user):
    return "<@" + str(user.id) + ">"

class Comie(discord.Client):
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
        global startdate
        startdate = datetime.utcnow()
        return

    async def on_member_join(self, member):
        await self.sendHelp(member, member)
        cmd = "INSERT INTO tblUser(uName, uID) VALUES ('%s','%s')" % (str(member), member.id)
        result = executeSql(cmd)
        return

    async def on_member_remove(self, member):
        cmd = "DELETE FROM tblUser WHERE uName = '%s' AND uID = '%s'" % (str(member), member.id)
        result = executeSql(cmd)
        return

    async def sendHelp(self, channel, requester):
        msg = ("Hi " + mentionUser(requester))
        msg = msg + "\nIch kann folgende Befehle bearbeiten:"
        msg = msg + "\n!help - Zeigt diese Hilfe an" 
        msg = msg + "\n!img - Schickt ein zufälliges Bild in den aktuellen Channel (Upvote: 👍 | Downvote: 👀)"
        msg = msg + "\n!roulette (!r) - Spielt Roulette"
        msg = msg + "\n!wichteln - Startet eine Wichtelpaar Auslosung"
        msg = msg + "\n!joke - Erzählt einen Witz"
        msg = msg + "\n!bugs - Gibt alle bekannten Fehler aus"
        msg = msg + "\n!coinflip - Wirft eine Münze"
        msg = msg + "\n!w [SeitenAnzahl] [WüfelAnzahl] - Wirft [WürfelAnzahl=1] Würfel mit [SeitenAnzahl] Seiten."
        msg = msg + "\n!a [Anime Name] [Streaming Link] [Tag1, Tag2, Tag3,...]- Fügt einen Anime zur Weebnation hinzu."
        msg = msg + "\n!w [Link]- Erstellt einen Watch2gether Link mit dem gewünschten Video."
        await channel.send(msg)

        return
    
    async def on_message(self, message):
        if message.author == self.user: 
            return
        
        if not message.content.startswith("!"):
            return
        
        if str(message.guild) == "None" and str(message.author) not in config["discord"]["admins"]:
            await message.channel.send("Ich reagiere nicht auf Befehle im privaten Chat! 😛")
            return

        message.content = str(message.content).lower()

        command = message.content.split(' ')[0][1:]

        ##### SECRET SANTA
        if command == "wichteln":
            if str(message.author) == config["secretsanta"]["organizer"]:
                await secretsanta.exec(self, message)
            else:
                await secretsanta.register(self, message)
            return

        elif command == "uptime":
            delta_uptime = datetime.utcnow() - startdate
            hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            msg = "Ich bin seit %d Tagen, %d Stunden und %d Minuten online! 😁" % (days, hours, minutes)
            await message.channel.send(msg)
            return

        #### ROULETTE
        elif command == "roulette" or command == "r":
            params = message.content.split(" ")[1:]
            accepted = ["stats","top","red","black","even","uneven","high","low","chart","give"]
            if len(params) == 0 or str(params[0]) == "help":
                await roulette.sendhelp(self, message.author)
                return
            elif params[0] == "stats":
                await roulette.sendstats(self, message)
                return
            elif params[0] == "top":
                await roulette.sendtoplist(self, message)
                return
            elif params[0] == "chart":
                await roulette.showchart(self, message)
                return
            elif params[0] == "give":
                await roulette.give(self, message)
                return
            elif not params[0].isnumeric() and params[0] not in accepted:
                await message.channel.send("Den Befehl kenne ich nicht. Unter !r help findest Du alle möglichen Befehle.")
                return
            else:
                if int(params[-1]) < 1:
                    await message.channel.send("Sorry %s, deine Bet muss mindestens 1 sein. 😟" % mentionUser(message.author))
                    return
                await roulette.play(self, message)
                return
            return

        elif command == "watch":
            params = message.content.split(" ")
            load = { 
                "w2g_api_key" : config["watchtogether"]["apikey"]
            }
            if len(params) != 1:
                load["share"] = params[-1]
            r = requests.post("https://w2g.tv/rooms/create.json", load)
            if r.status_code == 200:
                url = "https://w2g.tv/rooms/" + r.json()["streamkey"]
                await message.channel.send(url + " ist euer Watch2gether Raum. Viel Spaß! 🤗")
            else:
                print("ERROR in watch2gether api response")
            return

        ##### IMGUR
        elif command == "img":
            await message.channel.send("Hier kommt ein zufälliges Bild für dich %s ~(^__^)~" % (mentionUser(message.author)))
            await imgur.postImage(self, message, message.author)
            return

        elif command == "pro":
            #await message.channel.send("Hier kommt ein zufälliges pr0gramm Bild für dich %s ~(^__^)~" % (mentionUser(message.author)))
            #await imgur.postImage(self, message, message.author,"pro")
            return

        ##### IMGUR - RESULTS
        elif command == "results" and str(message.author) in config["discord"]["admins"]:
            results = await imgur.postResults(self, message.channel)
            winmsg = await message.channel.fetch_message(results[0])
            winner = await self.fetch_user(results[2])
            await message.channel.send("Gewonnen hat %s mit %d Votes für das gepinnte Bild!" % (mentionUser(winner), int(results[1])))
            await winmsg.pin()
            return

        #### JOKE
        elif command == "joke":
            await joker.exec(self, message)
            return

        #### GITHUB BUGS
        elif command == "bugs":
            await message.channel.send(git.exec(self))
            return

        ##### SELF HELP
        elif command == "help":
            await self.sendHelp(message.channel, message.author)
            return
        
        ## CSDATING
        elif command == "cs":
            params = message.content.split(" ")[1:]
            if len(params) == 0 or str(params[0]) == "help" or len(params) == 1:
                await csdating.sendhelp(self,message)
                return
            await csdating.datevote(self,message,int(params[0]),int(params[1]))
            return

        ##### COIN FLIP
        elif command == "coinflip":
            await coinflip.flip(message)
            return

        elif command == "w":
            await dice.exec(self,message)
            return

        # weebnation
        elif command == "a":
            try:
                if message.content.split(" ")[1] == "list":
                    #LIST 5 random ANIME
                    await weebnation.listAnimes(self, message)
                elif message.content.split(" ")[1] == "find":
                    #FIND ANIME (keyword in tags or name)
                    print(message.content)
                    await weebnation.findAnime(self, message)
                else:
                    # no second command 
                    await weebnation.addAnime(self, message)
            except:
                await message.channel.send("!a [Name] [Link] [Tag1,Tag2,...]")
            return

        ##### UNKNOWN COMMAND
        elif len(command) != 0:
            await message.channel.send("Den Befehl kenne ich nicht :/")
            return
