from discord import utils
import discord
import pymysql
import json
from datetime import datetime



class weebnation():
    async def addAnime(self, message):
        params = message.content.split(' ')[1:]
        link = [i for i in params if i.startswith('https://')][0]
        linkIndex = params.index(link)
        name = ' '.join(params[0:linkIndex])
        taglist = message.content.split(',')[0:]         # new split at comma
        taglist[0] = taglist[0].split(' ')[-1]      # delete the command, title and link
        tags = ''
        for i in range(len(taglist)):
            tags = tags + taglist[i].strip() + ', ' # strip the whitespaces 
        tags = tags[:-2]                            # delete the last 2 characters (comma and space
        if name == "" or link == "" or tags == "":
            await channel.send("Du musst den Namen, einen Link und mindestens einen Tag angeben!🤷🏼‍♂️")
            return
        else:
            cmd = "SELECT aTitle,aLink FROM tblAnime WHERE aTitle = '%s' OR aLink = '%s'" % (name, link)
            result = pymysql.executeSql(cmd)
            if len(result) > 0:
                 await message.channel.send("Der Anime ist bereits in der Weeb-Datenbank!🤷🏼‍♂️")
            else:
                cmd = "INSERT INTO tblAnime(aTitle, aLink, aCreator, aTags) VALUES ('%s','%s','%s','%s')" % (name, link, message.author.id, tags)
                pymysql.executeSql(cmd)
                cmd = "UPDATE tblUser SET uChips = uChips + 500 WHERE uID = '%s'" % (message.author.id)
                pymysql.executeSql(cmd)
                await message.channel.send("Ich habe %s der Weeb-Datenbank hinzugefügt." % (name))
            return

    async def listAnimes(self, message):
        cmd = "SELECT aTitle, aLink, aTags FROM tblAnime ORDER BY RAND() LIMIT 5"
        result = pymysql.executeSql(cmd)
        msg = "Hier 5 random Animes aus meiner Datenbank:\n"
        for i in range(len(result)):
            msg = msg + "%d. %s (%s) [%s]\n" % (i+1, result[i][0],result[i][1],result[i][2])
        await message.channel.send(msg)
        return

    async def findAnime(self,message):
        needle = message.content.split(" ")[2]
        if len(needle) <= 2:
            msg = "Yo, damit kann ich nicht anfangen... viel zu wenig :rolling_eyes: "
        elif len(needle) >= 32:
            msg = "Das ist mir zu viel zu suchen... :exploding_head: "
        else:
            needle = "%" + needle + "%"
            cmd = "SELECT aTitle, aLink FROM tblAnime WHERE aTags LIKE '%s' OR aTitle LIKE '%s'" % (needle, needle)
            result = pymysql.executeSql(cmd)
            print("found: ", len(result), "\n of max 3")
            if len(result) >= 1:
                msg = "Ich habe folgende Anime gefunden: 😁\n"

            cmd = 'SELECT aTitle,aLink FROM tblAnime WHERE aTags LIKE \'%' + needle + '%\' OR aTitle LIKE \'%' + needle + '%\''
            result = pymysql.executeSql(cmd)
            if result == None:
                await channel.send("🤕: Sorry, ich habe für dich gekämpft, aber ich habe keine Anime mit diesem Tag oder Titel gefunden...🏳️")
                return
            else:
                msg = "😁: Ich habe folgende Anime gefunden:\n"
                for i in range(len(result)):
                    msg = msg + result[i][0] + " :link: " + result[i][1] + "\n"
                    print(i)
                    if i+2 > 3:
                        break
            else:
                msg = "Sorry, ich habe für dich gekämpft, aber ich habe keinen passenden Anime gefunden... 🤕"
        await message.channel.send(msg)