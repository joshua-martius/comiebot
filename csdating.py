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
        await payload.channel.send("I han reagiert!")
        # Not quite sure if i understood the doku or handling right:'D Pretty sure that you can build it much smoother/slimmer
        #getting a list of the users that reacted to the certain message
        users = await self.reaction.users().flatten()
        #get the whole message information
        message = self.fetch_message(payload.message_id)
        #asking for 6 reactions(Bot reaction)
        if len(users) == 6:
            for user in users:
                msg = ("Hi **%s!**\n" % mentionUser(user))
                msg = msg +("Du hast ein Date um **%s**\n mit:" % (message.content))
                #call every user 
                for friend in users:
                    #skipping Rias(sadly(pls be real:( )))
                    if friend == "Rias" or friend == user:
                        continue
                    msg = msg +("%s" % (friend))
                    await user.send(msg)
                return
        return
