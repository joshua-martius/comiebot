import random
import statistics

def mentionUser(user):
    return "<@" + str(user.id) + ">"

def numericStringToEmoji(string):
    if "." in string:
        string = str(round(float(string)))
    if not string.isnumeric():
        return "NaN"
    output = ""
    for i in range(len(string)):
        switcher = {
            0: "0️⃣",
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣"
        }
        output = output + switcher.get(int(string[i]),"X")
    return output

class dice():
    async def exec(self, message):
        params = message.content.split(" ")[1:]
        if len(params) == 0 or not all(elem.isnumeric() for elem in params[1:]):
            await message.channel.send("Alle Parameter müssen Zahlen sein! 😑")
            return
        
        amount = 0
        maxInt = 0
        if len(params) == 1:
            amount = 1
            maxInt = int(params[-1])
        else: 
            amount = int(params[-1])
            maxInt = int(params[-2])

        if amount > 10 or amount < 1:
            await message.channel.send("Du kannst nur maximal 1 bis 10 Würfel gleichzeitig würfeln. 😅")
            return

        if maxInt > 100 or maxInt < 2:
            await message.channel.send("Ich generiere nur Zahlen von 2 bis 100. 😅")
            return

        results = []
        msg = "%s: " % (mentionUser(message.author))
        for rollIndex in range(amount):
            result = random.randint(1,maxInt)
            results.append(result)
            msg = msg + "\n%s" % (numericStringToEmoji(str(result)))

        if amount > 1:
            msg = msg + "\nSumme: %s" % (numericStringToEmoji(str(sum(results))))
            msg = msg + "\nDurchschnitt: %s" % (numericStringToEmoji(str(statistics.mean(results))))
        
        await message.channel.send(msg)
        return