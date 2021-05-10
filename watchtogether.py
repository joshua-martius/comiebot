import requests
from configwrapper import configwrapper

class watchtogether():
    async def exec(self, message):
        params = message.content.split(" ")
        roomLink = self.getRoom(params[-1])
        await message.channel.send(roomLink + " ist euer Watch2gether Raum. Viel Spaß! 🤗")
        return
    
    async def getRoom(videoid=""):
        load = { 
            "w2g_api_key" : configwrapper.getEntry("WATCH2GETHER_APIKEY")
        }
        if videoid != "" and videoid != "!watch":
            load["share"] = videoid
        r = requests.post("https://w2g.tv/rooms/create.json", load)
        if r.status_code == 200:
            url = "https://w2g.tv/rooms/" + r.json()["streamkey"]
            return url
        else:
            print("ERROR in watch2gether api response")        
        return "ERROR"