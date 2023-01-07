from discord import utils
import json
import discord

config = json.loads(open("./config.json","r").read())
processedMessages = {}


def mentionUser(user):
    return "<@" + str(user.id) + ">"

class csdating():
    async  def datevote(self,message,start_time, end_time):
        if start_time > end_time or start_time < 1 or end_time > 24:
            await message.channel.send("Bitte gib eine gültige Zeit an! 🥲")
            return

        if abs(start_time - end_time) > 4:
            await message.channel.send("Der Zeitrahmen darf nicht größer als 4 Stunden sein! 🥹")
            return
        
        # time frame is valid, going on...
        await message.channel.send("%s möchte heute CS:GO spielen @everyone, wann habt ihr Zeit? 🔥🔥🔥" % (mentionUser(message.author)))
        for i in range(start_time,end_time + 1):
            reactionMessage = await message.channel.send(str(i) + " Uhr")
            await reactionMessage.add_reaction('❌')
            await reactionMessage.add_reaction('✅')
        await message.delete()
        processedMessages[message.id] = False

    async  def sendhelp(self,message):
        msg = "*So benutzt du CSDating:*"
        msg = msg + "\n-->: !cs Start Zeit End Zeit"
        msg = msg + "\n-->: Beispiel: !cs 19 21" 
        msg = msg + "\n-->: Damit werden 3 Nachrichten mit den Zeiten 19 Uhr,20 Uhr und 21 Uhr schon mit Reactions gesendet!"
        await message.channel.send(msg)

    async def reaction(self,payload):
        #Get the Full message data without the fix channel
        for channel in self.guilds[0].channels:
            if channel.name == config["csgo"]["channelName"]:
                message = await channel.fetch_message(payload.message_id)

        # check if the message has already been processed
        try:
            if processedMessages[message.id] == True:
                return
        except:
            # message has not been processed yet, do nothing
            pass

        # iterate over the reaction
        for reaction in message.reactions:
            # Full team accepted.
            if reaction.emoji != "✅":
                continue

            if reaction.count == 2:
                # remove bot's own reaction from the message
                await message.remove_reaction("✅", self.member)

            if reaction.count == 5:
                #Create a list of the users that reacted to the message
                users = await reaction.users().flatten()

                #iterate over the users
                for user in users:
                    msg = ("Hi **%s!**\n" % mentionUser(user))
                    msg = msg +("Du hast ein Date um **%s** mit:\n" % (message.content))
                    #mention the teammates for user
                    for teammate in users:
                        #dont mention the bot and the user himself
                        if teammate.name == config["discord"]["botName"] or teammate.name == user.name:
                            continue
                        msg = msg +("%s \n" % (teammate.name))
                    #send Message to the user
                    if user.name != config["discord"]["botName"]:
                        await user.send(msg)

                processedMessages[message.id] = True
        return
