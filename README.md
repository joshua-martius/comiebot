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
        "rolename": ""
    }
}
```
## Installation:
### Python package requirements
*Python >3.6*
- pip install discord.py
- pip install pillow
- pip install python-git
- pip install requests
- pip install mysql-connector-python
- pip install kaleido
- pip install plotly

### Database
- MySQL
