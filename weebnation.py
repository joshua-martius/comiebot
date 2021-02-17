from discord import utils
import discord
import mysql.connector
import json
from datetime import datetime

config = json.loads(open("./config.json","r").read())

mydb = mysql.connector.connect(
  host=config["db"]["host"],
  user=config["db"]["user"],
  password=config["db"]["password"],
  database=config["db"]["name"]
)

sql = mydb.cursor()


def executeSql(cmd):
    mydb.connect()
    print("Executing: " + cmd)
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

class webnation():
    
    async  def addAnime(self, message, channel ,name, link,  tags):
        if name == None or link == None or tags == None:
            await channel.send("Du musst den Namen einen Link und mindestens einen Tag angeben!🤷🏼‍♂️")
            return
        else:
            cmd = "SELECT aTitle,aLink FROM tblAnime WHERE aTitle = '%s' OR aLink = '%s'" % (name, link)
            result = executeSql(cmd)
            if result == None:
                 await channel.send("Der Anime ist bereits in der Weeb-Datenbank!🤷🏼‍♂️")
                 return
            else:
                timestamp = datetime.now()
                cmd = "INSERT INTO tblAnime(aTitle, aLink, aCreator, aCreatedAt, aTags) VALUES ('%s','%s')" % (name, link, message.author, timestamp, tags)
                executeSql(cmd)

    async def showAnimes(self,message):
        await channel.send("Hier ist der Link zum Himmel!")
        await channel.send(link)