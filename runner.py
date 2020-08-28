import comie

token = ""
try:
    with open(".token","r") as file:
        token = file.readline()
        if token == "":
            print("No token given. Exiting.")
            exit()
except:
    print("No .token file found. Exiting.")
    exit()
    
bot = comie.Comie()
bot.run(token)