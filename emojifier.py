def isUniqueChars(st):
    char_set = [False] * 128
    for i in range(0, len(st)):
        val = ord(st[i])
        if char_set[val]:
            return False
        char_set[val] = True
    return True

def getEmojiByChar(char):
    # todo: find best solution to model dictionary
    return "🇦"

class emojifier():

    async def exec(self, message):
        channel = message.channel
        messageRaw = await channel.history(limit=2).flatten()
        message = messageRaw[-1]
        string = message.content.split(" ")[-1]
        if not isUniqueChars(string):
            await channel.send("Das Wort darf jeden Buchstaben nur einmal haben :/")
            return
        for c in string:
                await message.add_reaction(getEmojiByChar(c))
        return