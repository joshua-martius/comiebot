
from discord import utils
import random
import json

config = json.loads(open("./config.json","r").read())

def mentionUser(user):
    return "<@" + str(user.id) + ">"

class secretsanta():

    async def register(self, message):
        role = utils.get(message.guild.roles, name=config["secretsanta"]["rolename"])
        user = message.author
        try:
            if role not in user.roles:
                await user.add_roles(role)
                await message.channel.send("Super %s! Du bist jetzt fürs Wichteln angemeldet. 🤭" % (mentionUser(message.author)))
            else:
                await message.channel.send("%s, du bist fürs Wichteln schon angemeldet! 😁" % (mentionUser(message.author)))
        except:
            await message.channel.send("Ich hab leider nicht die Rechte dich zum Wichteln anzumelden :(")
        return

    async def exec(self, message):
        debug = message.content.endswith("debug")
        try:
            users = message.guild.members
        except:
            await message.author.send("Wichteln kann nicht aus einem privaten Chat heraus gestartet werden!")
            return

        role = utils.get(message.guild.roles, name=config["secretsanta"]["rolename"])
        santas = []
        for u in users:
            if role in u.roles:
                santas.append(u)
        
        if len(santas) < 3:
            await message.channel.send("Mindestens drei Leute müssen die Rolle \"" + config["secretsanta"]["rolename"] + "\" besitzen... :/")
            return

        await message.channel.send("Los gehts! %s Leute nehmen Teil!" % (len(santas)))
        
        random.seed(random.randint(1, 1000))
        shuffles = random.randint(1,10)
        for i in range(shuffles):
            random.shuffle(santas) # randomize the list
        
        if not debug:
            for i in range(len(santas) - 1):
                santaFrom = santas[i]
                santaTo = mentionUser(santas[i + 1])
                await santaFrom.send("Dein Wichtelpartner ist: " + santaTo)

            # Special message for the last entry
            await santas[-1].send("Dein Wichtelpartner ist: " + str(santas[0]))
        else:
            for i in range(len(santas) - 1):
                santaFrom = santas[i]
                santaTo = santas[i + 1]
                await message.channel.send("%s hat %s bekommen." % (mentionUser(santaFrom), mentionUser(santaTo)))
            await message.channel.send("%s hat %s bekommen." % (mentionUser(santas[-1]), mentionUser(santas[0])))

        await message.channel.send("Ich habe die Teilnehmerliste %d mal durchgewürfelt :)" % (shuffles))
        await message.channel.send("Partnervergabe abgeschlossen! Viel Spaß %ss!" % (config["secretsanta"]["rolename"]))
        return
    