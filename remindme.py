import pymysql
from datetime import datetime, timedelta
from asyncio import sleep

from configwrapper import configwrapper

class remindme():
    async def addReminder(message):
        userid = message.author.id
        split = message.content.split(" ")[1:]
        topic = ' '.join(split[1:])
        timestring = split[0].replace(",",".") # damn you americans
        if ":" not in timestring:
            num = float(timestring[0:-1])
            unit = timestring[-1]
            remindertime = ""
            if unit == "h":
                remindertime = datetime.now() + timedelta(hours=num)
            elif unit == "m":
                remindertime = datetime.now() + timedelta(minutes=num)
            else:
                await message.channel.send("Ich kann nur Minuten (m) und Stunden (h) verarbeiten :/")
                return
        else:
            today = datetime.now()
            remindertime = today.replace(hour=int(timestring.split(":")[0]),minute=int(timestring.split(":")[1]))
        
        cmd = "INSERT INTO tblReminder(rUserID,rTopic,rTime) VALUES ('%s','%s','%s')" % (userid, topic, remindertime.strftime("%Y-%m-%d %H:%M"))
        pymysql.executeSql(cmd)
        await message.channel.send("Okay, ich erinnere dich um %s an %s! :)" % (remindertime.strftime("%H:%M"), topic))
        return

    async def extendReminder(self, messageID: str):
        extensionTime = configwrapper.getEntry("REMINDER_EXTENSION_TIME")
        cmd = "SELECT rUserID FROM tblReminder WHERE rMessageID = '%s'" % (messageID)
        result = pymysql.executeSql(cmd)
        user = await self.fetch_user(result[0][0])
        cmd = "UPDATE tblReminder SET rSentOut = 0, rTime = DATE_ADD(rTime, INTERVAL %s MINUTE) WHERE rMessageID = '%s'" % (extensionTime,messageID)
        pymysql.executeSql(cmd)
        await user.send("Okay, ich erinnere dich in %s Minuten nochmal! :)" % (extensionTime))
        return

    async def init(self):
        # wait for reminders
        print("Starting Reminder module at full minute.")
        sleeptime = 60 - datetime.utcnow().second
        await sleep(sleeptime)
        print("Starting Reminder module.")
        while True:
            cmd = "SELECT rID, rUserID, rTime, rTopic FROM tblReminder WHERE rTime LIKE '%%%s%%' AND rSentOut = 0" % (datetime.now().strftime("%Y-%m-%d %H:%M"))
            result = pymysql.executeSql(cmd)
            for row in result:
                user = await self.fetch_user(row[1])
                try:
                    timetext = datetime.strptime(row[2],"%Y-%m-%d %H:%M:%S")
                except:
                    timetext = datetime.strptime(row[2],"%Y-%m-%d %H:%M")
                message = await user.send("Es ist %s Uhr, ich erinnere dich an: %s! :)" % (timetext.strftime("%H:%M"),row[3]))
                await message.add_reaction('🔁')
                cmd = "UPDATE tblReminder SET rSentOut = 1, rMessageID = '%s' WHERE rID = %d" % (message.id,int(row[0]))
                pymysql.executeSql(cmd)
            await sleep(60)
        return