from discord import utils
import discord

def mentionUser(user):
    return "<@" + str(user.id) + ">"

class csdating():

    async  def datevote(self,channel,start_time, end_time):
        await channel.send("Oke wann habt ihr Zeit?<@everybody>")
        for i in range(start_time,end_time):
            message = await channel.send(i+"Uhr")
            message.add_reaction('👍🏻')
            message.add_reaction('👎🏻')


    async  def sendhelp(self,channel):
        msg = ("Hi **%s!**" % mentionUser(channel.author))
        msg = msg + "\n*So benutzt du CSDating:*"
        msg = msg + "\n-->: !cs Start Zeit End Zeit"
        msg = msg + "\n-->: Beispiel: !cs 19 21" 
        msg = msg + "\n-->: Damit werden 3 Nachrichten mit den Zeiten 19 Uhr,20 Uhr und 21 Uhr schon mit Reactions gesendet!"
        await channel.send(msg)
        