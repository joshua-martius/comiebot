import discord
import random
adminName = "y0sh1#1990"
santaRoleName = "Wichtel"
guildId = 1 # 1 = testbench | 0 = conies homies

class Comie(discord.Client):
    async def on_ready(self):
        print("Bot is up and running.")
        return
    
    async def on_message(self, message):
        if message.author == self.user:
            return

        ##### SECRET SANTA
        if message.content.startswith("!wichteln") and str(message.author) == adminName:
            debug = message.content.endswith("debug")
            users = self.guilds[guildId].members
            role = discord.utils.get(self.guilds[guildId].roles, name=santaRoleName)
            santas = []
            for u in users:
                if role in u.roles:
                    santas.append(u)
            
            if len(santas) < 3:
                await message.channel.send("Mindestens drei Leute müssen die Rolle \"" + santaRoleName + "\" besitzen... :/")
                return

            await message.channel.send("Los gehts! %s Leute nehmen Teil!" % (len(santas)))
            
            shuffles = random.randint(1,10)
            for i in range(shuffles):
                random.shuffle(santas) # randomize the list
            
            if not debug:
                for i in range(len(santas) - 1):
                    santaFrom = santas[i]
                    santaTo = str(santas[i + 1])
                    await santaFrom.send("Dein Wichtelpartner ist: " + santaTo)

                # Special message for the last entry
                await santas[-1].send("Dein Wichtelpartner ist: " + str(santas[0]))
            else:
                for i in range(len(santas) - 1):
                    santaFrom = str(santas[i])
                    santaTo = str(santas[i + 1])
                    await message.channel.send("%s hat %s bekommen." % (santaFrom, santaTo))
                await message.channel.send("%s hat %s bekommen." % (str(santas[-1]), str(santas[0])))

            await message.channel.send("Ich habe die Teilnehmerliste %d mal durchgewürfelt :)" % (shuffles))
            await message.channel.send("Partnervergabe abgeschlossen! Viel Spaß!")
            return
        #####


        if message.content.startswith("!help"):
            id = message.author.id
            await message.channel.send("Hi <@" + str(id) + ">!\nLeider kann ich noch nichts :(")
            return