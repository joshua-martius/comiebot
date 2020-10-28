import comie
import json

config = json.loads(open("./config.json","r").read())
    
bot = comie.Comie()
bot.run(config["discord"]["token"])