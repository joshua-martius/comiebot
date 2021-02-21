# Conies Homies Discord Bot
A small discordpy based bot for our little community.

## Modules
### Git
Downloads all Issues with a "Bug" tag and prints them into the current channel.
### Joker
Sends a random Joke into the current channel.
### Imgur
Sends a random Imgur image into the current channel.
### Roulette (Beta)
Plays Roulette with the players
### Secret Santa
Gives every user with a specified role a secret santa.
### Uptime
Sends the time since the bot has started into the current channel.
### Coinflip
Flips a coin
### Dice
Throws a dice, see !help for usage.
### CSDating
Want to know when your friends got time for CSGO? Make Comie ask them for you.
### Watch2Gether
Create watch2gether rooms with a preloaded video
### Weebnation
Share a list of series you would recommend to your friends

## Configuration
A local config.json has to exist in the following form:
```
{
    "discord":{
        "token": "",
        "admins": ["",""]
    },
    "db": {
        "host": "",
        "user": "",
        "password": "",
        "name": ""
    },
    "roulette":
    {
        "maxbet": -1
    },
    "secretsanta":
    {
        "rolename": "",
	"organizer": ""
    },
    "watchtogether":
    {
        "apikey": ""
    }
}
```
## Installation:
### Python package requirements
*Python >3.6*
- pip3 install discord.py
- pip3 install pillow
- pip3 install python-git
- pip3 install requests
- pip3 install mysql-connector-python
- pip3 install kaleido
- pip3 install plotly

### Database
- MySQL

Hello World, again :)
