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
            await message.add_reaction('✋🏻')
            await message.add_reaction('👍🏻')

    async  def sendhelp(self,message):
        msg = "*So benutzt du CSDating:*"
        msg = msg + "\n-->: !cs Start Zeit End Zeit"
        msg = msg + "\n-->: Beispiel: !cs 19 21" 
        msg = msg + "\n-->: Damit werden 3 Nachrichten mit den Zeiten 19 Uhr,20 Uhr und 21 Uhr schon mit Reactions gesendet!"
        await message.channel.send(msg)
        
