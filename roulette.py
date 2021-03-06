from discord import utils
import discord
import random
import string
import urllib.request
from PIL import Image
import pymysql
import plotly.graph_objects as go
import json

# False = Black
# True = Red
board = {
    1: True,
    2: False,
    3: True,
    4: False,
    5: True,
    6: False,
    7: True,
    8: False,
    9: True,
    10: False,
    11: False,
    12: True,
    13: False,
    14: True,
    15: False,
    16: True,
    17: False,
    18: True,
    19: True,
    20: False,
    21: True,
    22: False,
    23: True,
    24: False,
    25: True,
    26: False,
    27: True,
    28: False,
    29: False,
    30: True,
    31: False,
    32: True,
    33: False,
    34: True,
    35: False,
    36: True
}

config = json.loads(open("./config.json","r").read())


def getUserFromString(message):
    return message[3:-1]

def mentionUser(user):
    return "<@" + str(user.id) + ">"

async def giveplayerchips(user, chips):
    if await isplayerregistered(user):
        cmd = "UPDATE tblUser SET uChips = uChips + %d WHERE uID = '%s'" % (chips, user.id)
        pymysql.executeSql(cmd)
    return

async def getplayerchips(user):
    cmd = "SELECT uChips FROM tblUser WHERE uID = '%s'" % (user.id)
    chips = int(pymysql.executeSql(cmd)[0][0])
    return chips

async def isplayerregistered(user):
    cmd = "SELECT uName FROM tblUser WHERE uID = '%s'" % (user.id)
    return (len(pymysql.executeSql(cmd)) != 0)

async def registerplayer(user):
    try:
        cmd = "INSERT INTO tblUser(uName, uID) VALUES ('%s','%s')" % (str(user), str(user.id))
        pymysql.executeSql(cmd)
        return True
    except:
        return False

async def getplayerstats(user):
    cmd = "SELECT uChips, uCreated FROM tblUser WHERE uID = '%s'" % (user.id)
    return pymysql.executeSql(cmd)[0]

# [Win, WinAmount, WinningNumber, IsRed]
async def checkforwin(user, params):
    rnd = random.randint(0,35)
    bet = int(params[-1])

    if rnd == 0 and params[0].isnumeric() and int(params[0]) == 0:
        win = bet + (bet * 35)
        await giveplayerchips(user, win)
        return [True, win, 0, False]

    rnd = rnd + 1
    result = board[rnd]

    if params[0].isnumeric() and int(params[0]) < 37 and int(params[0]) >= 0 and rnd == int(params[0]):
        win = bet + (bet * 35)
        await giveplayerchips(user, win)
        return [True, win, rnd, result]
    if params[0] == "black" and result == False:
        win = bet * 2
        await giveplayerchips(user, win)
        return [True, win, rnd, result]
    elif params[0] == "red" and result == True:
        win = bet * 2
        await giveplayerchips(user, win)
        return [True, win, rnd, result]
    elif params[0] == "high" and rnd >= 19:
        win = bet * 2
        await giveplayerchips(user, win)
        return [True, win, rnd, result]
    elif params[0] == "low" and rnd <= 18 and rnd != 0:
        win = bet * 2
        await giveplayerchips(user, win)
        return [True, win, rnd, result]
    elif params[0] == "even" and rnd % 2 == 0:
        win = bet * 2
        await giveplayerchips(user, win)
        return [True, win, rnd, result]
    elif params[0] == "uneven" and rnd % 2 != 0:
        win = bet * 2
        await giveplayerchips(user, win)
        return [True, win, rnd, result]
    else:
        return [False, bet, rnd, result]

class roulette():

    async def sendhelp(self, user):
        msg = ("Hi **%s!**" % mentionUser(user))
        msg = msg + "\n*So spielst du Roulette:*"
        msg = msg + "\n>Einfache Bets (2:1) Gewinn):" 
        msg = msg + "\n-->!r red/black [Bet] - Setzt [Bet] Chips auf Rot oder Schwarz"
        msg = msg + "\n-->!r even/uneven [Bet] - Setzt [Bet] Chips auf die Gerade oder Ungeraden Zahlen"
        msg = msg + "\n-->!r high/low [Bet] - Setzt [Bet] Chips auf die hohen (19-36) oder niedrigen (1-18) Zahlen"
        msg = msg + "\n>Mehrfache Bets (Verschiedene Gewinne):"
        msg = msg + "\n-->!r [0,1,...,37] [Bet] - Setzt [Bet] Chips auf eine bestimmte Zahl. (Gewinn: 35:1)"
        await user.send(msg)
        msg = "*>Weitere Befehle sind:*"
        msg = msg + "\n-->!r stats - Zeigt deine Statistik an"
        msg = msg + "\n-->!r top - Zeigt die aktuelle Toplist an."
        msg = msg + "\n-->!r give [@ user] [Chips] gibt [User] [Chips] aus dem eigenen Konto."
        msg = msg + "\n-->!r chart zeigt auf eine Auswertung."
        await user.send(msg)
        return

    async def sendstats(self, message):
        stats = await getplayerstats(message.author)
        msg = "Hi %s! Hier sind deine Statistiken:\nChips: %d\nRegistriert seit: %s" % (mentionUser(message.author), stats[0], stats[1])
        await message.channel.send(msg)
        return

    async def sendtoplist(self, message):
        cmd = "SELECT uChips, uID FROM tblUser ORDER BY uChips DESC LIMIT 3"
        result = pymysql.executeSql(cmd)
        msg = "Die aktuell %d besten Roulette Spieler:\n" % (len(result))
        for i in range(len(result)):
            user = await self.fetch_user(result[i][1])
            msg = msg + "%d. %s (%d Chips)\n" % ((i+1), mentionUser(user), result[i][0])
        await message.channel.send(msg)
        return

    async def showchart(self, message):
        cmd = "SELECT uName, uChips FROM tblUser ORDER BY uChips DESC"
        result = pymysql.executeSql(cmd)
        labels = []
        values = []
        for row in result:
            labels.append(row[0][:row[0].index("#")])
            values.append(row[1])
        
        fig = go.Figure([go.Bar(x=labels,y=values)])
        fig.write_image("./chart.png")
        await message.channel.send(file=discord.File('chart.png'))
        return

    async def give(self, message):
        user = message.author
        msg = message.content
        params = msg.split(" ")[1:]
        receiver = ""
        if params[1] != "@everyone":
            receiver = await self.fetch_user(getUserFromString(params[1]))
        amount = int(params[-1])
        userbalance = await getplayerchips(user)

        if userbalance < amount:
            await message.channel.send("Sehr löblich von dir %s, aber du kannst nicht mehr Chips ausgeben als du besitzt (%d)." % (mentionUser(user), userbalance))
            return
        elif amount < 1:
            await message.channel.send("Netter Versuch.... %s ...zur Strafe ziehe ich dir 10 Chips ab!" % (mentionUser(user)))
            await giveplayerchips(user, -10)
        elif params[1] not in "@everyone" and not await isplayerregistered(receiver):
            await message.channel.send("Sorry, %s. %s ist nicht fürs Roulette angemeldet." % (mentionUser(user), mentionUser(receiver)))
            return
        else:
            if params[1] != "@everyone":
                await giveplayerchips(user, -amount)
                await giveplayerchips(receiver, amount)
                await message.channel.send("%s hat %s %d Chips gegeben. 🦕 " % (mentionUser(user), mentionUser(receiver), amount))
            else:
                receivers = []
                users = message.channel.guild.members
                for u in users:
                    if str(u.status) == "offline" or u.bot or u == user or not await isplayerregistered(u):
                        continue
                    else:
                        receivers.append(u)
                
                if len(receivers) * amount > userbalance:
                    await message.channel.send("Sehr löblich von dir %s, aber du kannst dir nicht leisten allen soviel zu schenken." % (mentionUser(user)))
                    return
                else:
                    await giveplayerchips(user, -(len(receivers) * amount))
                    for u in receivers:
                        await giveplayerchips(u, amount)
                    
                    await message.channel.send("🍾🍾🍾 %s hat allen %d Online-Spielern %d Chips geschenkt!!! 🍾🍾🍾" % (mentionUser(user), len(receivers) ,amount))
            return

    async def play(self, message):
        user = message.author
        if not await isplayerregistered(user):
            await registerplayer(user)
            await message.channel.send("Das hier scheint dein erstes Spiel zu sein, %s! Du startest mit 1.000 Chips! 🤗" % mentionUser(message.author))

        msg = message.content.lower()
        params = msg.split(" ")[1:]
        bet = int(params[-1])
        currentchips = await getplayerchips(user)
        if bet > currentchips:
            await message.channel.send("Sorry %s, du kannst keine %d Chips wetten wenn du nur %d hast. 😅" % (mentionUser(user), bet, currentchips))
            return
        elif config["roulette"]["maxbet"] != -1 and bet > config["roulette"]["maxbet"]:
            await message.channel.send("Sorry %s, aktuell kann man nur maximal %d Chips setzen." % (mentionUser(user), config["roulette"]["maxbet"]))
            return
        
        win = await checkforwin(user, params)

        if not win[0]:
            if win[3]:
                await message.channel.send("Sorry %s, die Kugel landete auf %d Rot. 😅 Du verlierst deine %d Chips. 😐" % (mentionUser(user), win[2], bet))
            else:
                await message.channel.send("Sorry %s, die Kugel landete auf %d Schwarz. 😅 Du verlierst deine %d Chips. 😐" % (mentionUser(user), win[2], bet))

            await giveplayerchips(user, -bet)
        else:
            if win[3]:
                await message.channel.send("✨✨✨ Glückwunsch %s!!! Du hast mit der Wette auf %d Rot !!%d!! Chips gewonnen! 🍾🍾🍾" % (mentionUser(user), win[2] , win[1]))
            else:
                await message.channel.send("✨✨✨ Glückwunsch %s!!! Du hast mit der Wette auf %d Schwarz !!%d!! Chips gewonnen! 🍾🍾🍾" % (mentionUser(user), win[2] , win[1]))
        return
