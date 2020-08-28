import comie

token = ""
with open(".token","r") as file:
    token = file.readline()
    if token == "":
        print("No token given. Exiting.")
        exit()

bot = comie.Comie()
bot.run(token)