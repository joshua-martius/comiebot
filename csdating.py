from discord import utils
import discord

def mentionUser(user):
    return "<@" + str(user.id) + ">"

class csdating():
    async  def datevote(self,message,start_time, end_time):
        await message.channel.send("%s möchte heute CS:GO spielen @everyone, wann habt ihr Zeit?" % (mentionUser(message.author)))
        for i in range(start_time,end_time + 1):
            message = await message.channel.send(str(i) + " Uhr")
            await message.add_reaction('👎🏻')
            await message.add_reaction('👍🏻')

    async  def sendhelp(self,message):
        msg = "*So benutzt du CSDating:*"
        msg = msg + "\n-->: !cs Start Zeit End Zeit"
        msg = msg + "\n-->: Beispiel: !cs 19 21" 
        msg = msg + "\n-->: Damit werden 3 Nachrichten mit den Zeiten 19 Uhr,20 Uhr und 21 Uhr schon mit Reactions gesendet!"
        await message.channel.send(msg)
        

    async def reaction(self,payload):
        #Get the Full message data 
        message = await self.guilds[0].channels[2].fetch_message(payload.message_id)
        #iterate over the reaction
        for reaction in message.reactions:
            #Full team accepted. (6 because of the Bot)
            if reaction.emoji == "👍🏻" and reaction.count == 6:
                #Create a list of the users that reacted to the message
                users = await reaction.users().flatten()
                #iterate over the users
                for user in users:
                    msg = ("Hi **%s!**\n" % mentionUser(user))
                    msg = msg +("Du hast ein Date um **%s** mit:\n" % (message.content))
                    #mention the teammates for user
                    for teammate in users:
                        #dont mention the bot and the user himself
                        if teammate.name == "Rias" or teammate.name == user.name:
                            continue
                        msg = msg +("%s \n" % (teammate.name))
                    #send Message to the user
                    await user.send(msg)
        return