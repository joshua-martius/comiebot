import discord
import pymysql
from discord import utils

class rolehandler():
    async def init(self):
        # ToDo: search channel instead of hardcoding it
        message = await self.guilds[0].channels[-2].fetch_message(pymysql.config["roles"]["reactionMessage"])
        for key, value in pymysql.config["roles"]["list"].items():
            await message.add_reaction(value)
        print("Initialized rolehandler.")
        return

    async def reactionAdded(self, userid, emojiname, messageid):
        # find role associated to emoji
        message = await self.guilds[0].channels[-2].fetch_message(pymysql.config["roles"]["reactionMessage"])
        for key, value in pymysql.config["roles"]["list"].items():
            if value == str(emojiname):
                role = utils.get(message.guild.roles, name=key)
                break

        # give user the found role
        try:
            user = utils.get(self.get_all_members(), id=userid)
            await user.add_roles(role)
        except:
            print("Tried to give role that doesnt exist.")
        return

    async def reactionRemoved(self, userid, emojiname, messageid):
        # find role associated to emoji
        message = await self.guilds[0].channels[-2].fetch_message(pymysql.config["roles"]["reactionMessage"])
        for key, value in pymysql.config["roles"]["list"].items():
            if value == str(emojiname):
                role = utils.get(message.guild.roles, name=key)
                break
                
        # take user the found role
        try:
            user = utils.get(self.get_all_members(), id=userid)
            await user.remove_roles(role)
        except:
            print("Tried to take role that doesnt exist.")
        return