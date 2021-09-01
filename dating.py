from discord import utils
import json
import discord
import pymysql

config = json.loads(open("./config.json","r").read())

def mentionUser(user):
    return "<@" + str(user.id) + ">"

class dating():
    async  def datevote(self,message,start_time, end_time):
        await message.channel.send("%s möchte heute %s spielen @everyone, wann habt ihr Zeit?" % (mentionUser(message.author),message.channel.name))
        for i in range(start_time,end_time + 1):
            reactionMessage = await message.channel.send(str(i) + " Uhr")
            await reactionMessage.add_reaction('❌')
            await reactionMessage.add_reaction('✅')
        await message.delete()

    async  def sendhelp(self,message):
        msg = "*So benutzt du Dating:*"
        msg = msg + "\n-->: !d Start Zeit End Zeit"
        msg = msg + "\n-->: Beispiel: !d 19 21" 
        msg = msg + "\n-->: Damit werden 3 Nachrichten mit den Zeiten 19 Uhr,20 Uhr und 21 Uhr schon mit Reactions gesendet!"
        await message.channel.send(msg)

    async def reaction(self,payload):
        cmd = "SELECT gName FROM tblGame WHERE gChannelID = %s " (payload.channelid)
        result = pymysql.executeSql(cmd)
        #Get the Full message data without the fix channel
        for channel in self.guilds[0].channels:
            if channel.name == result:
                message = await channel.fetch_message(payload.message_id)

        cmd = "SELECT gTeamsize FROM tblGame WHERE gChannelID = %s " (payload.channelid)
        result = pymysql.executeSql(cmd)
        #iterate over the reaction
        for reaction in message.reactions:
            #Full team accepted.
            if reaction.emoji == "✅": 
                if reaction.count >= 2:
                    # remove bot's own reaction from the message
                    await message.remove_reaction("✅", self.member)
                if reaction.count == result:
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
        return
