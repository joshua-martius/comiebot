from discord import utils
import discord
import random
import string
import urllib.request
from PIL import Image
import mysql.connector

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

dbcred = []
try:
    with open("./.dbcred") as file:
        for i in range(4):
            line = file.readline()
            dbcred.append(line.strip('\n'))
except:
    print("Couldnt find database credentials in .dbcred file. Exiting.")
    exit()

mydb = mysql.connector.connect(
  host=dbcred[0],
  user=dbcred[1],
  password=dbcred[2],
  database=dbcred[3]
)

sql = mydb.cursor()

def executeSql(cmd):
    mydb.connect()
    print("Executing:: " + cmd)
    if cmd.startswith("SELECT"):
        sql.execute(cmd)
        result = sql.fetchall()
        mydb.close()
        return result
    else:
        # insert, update or delete
        sql.execute(cmd)
        mydb.commit()
        mydb.close()
        return

def mentionUser(user):
    return "<@" + str(user.id) + ">"

async def giveplayerchips(user, chips):
    cmd = "UPDATE tblUser SET uChips = uChips + %d WHERE uID = '%s'" % (chips, user.id)
    executeSql(cmd)
    return

async def getplayerchips(user):
    cmd = "SELECT uChips FROM tblUser WHERE uID = '%s'" % (user.id)
    chips = int(executeSql(cmd)[0][0])
    return chips

async def isplayerregistered(user):
    cmd = "SELECT uName FROM tblUser WHERE uID = '%s'" % (user.id)
    return (len(executeSql(cmd)) != 0)

async def registerplayer(user):
    try:
        cmd = "INSERT INTO tblUser(uName, uID) VALUES ('%s','%s')" % (str(user), str(user.id))
        executeSql(cmd)
        return True
    except:
        return False

async def getplayerstats(user):
    cmd = "SELECT uChips, uCreated FROM tblUser WHERE uID = '%s'" % (user.id)
    return executeSql(cmd)[0]

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
        msg = "Hi %s!\nSo spielst du Roulette:\n->Einfache Bets (1:2 Gewinn):\n" % mentionUser(user)
        msg = msg + "-->!r red/black [Bet] - Setzt [Bet] Chips auf Rot oder Schwarz\n-->!r even/uneven [Bet] - Setzt [Bet] Chips auf die Gerade oder Ungeraden Zahlen"
        msg = msg + "\n-->!r high/low [Bet] - Setzt [Bet] Chips auf die hohen (19-36) oder niedrigen (1-18) Zahlen"
        msg = msg + "\n->Mehrfache Bets (Verschiedene Gewinne):\n-->!r [0,1,...,37] [Bet] - Setzt [Bet] Chips auf eine bestimmte Zahl. (Gewinn: 35:1)"
        await user.send(msg)
        await user.send("Weitere Befehle sind:\n!r stats - Zeigt deine Statistik an\n!r top - Zeigt die aktuelle Toplist an.")
        await user.send("\n-->!r give KnuT#7402 [Chips] gibt dem Benutzer Knut#7402 Chips aus dem eigenen Konto.")
        await user.send("\n-->!r chart zeigt auf eine Auswertung an.")
        return

    async def sendstats(self, message):
        stats = await getplayerstats(message.author)
        msg = "Hi %s! Hier sind deine Statistiken:\nChips: %d\nRegistriert seit: %s" % (mentionUser(message.author), stats[0], stats[1])
        await message.channel.send(msg)
        return

    async def sendtoplist(self, message):
        cmd = "SELECT uChips, uID FROM tblUser ORDER BY uChips DESC LIMIT 3"
        result = executeSql(cmd)
        msg = "Die aktuell %d besten Roulette Spieler:\n" % (len(result))
        for i in range(len(result)):
            user = await self.fetch_user(result[i][1])
            msg = msg + "%d. %s (%d Chips)\n" % ((i+1), mentionUser(user), result[i][0])
        await message.channel.send(msg)
        return

    async def showchart(self, message):
        msg ="https://link-to-chart.tld/page.php?nothing=something"
        await message.channel.send(msg)
        return

    async def give(self, message):
        user = message.author
        msg = message.content
        params = msg.split(" ")[1:]
        receiver = params[1]
        amount = int(params[-1])
        if getplayerchips(user) < amount:
            await message.channel.send("Sehr löblich von dir %s, aber du kannst nicht mehr Chips ausgeben als du besitzt (%d)." % (mentionUser(user), currentchips))
            return
        elif amount < 1:
            await message.channel.send("Netter Versuch.... %s ...zur Strafe ziehe ich dir 10 Chips ab!" % (mentionUser(user)))
            await giveplayerchips(user, -10)
        else:
            await giveplayerchips(user, -amount)
            await giveplayerchips(receiver, amount)
            await message.channel.send("%s hat %s %d gegeben. 🦕 " % (user, receiver, amount))
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
