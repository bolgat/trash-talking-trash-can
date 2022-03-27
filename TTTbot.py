import matplotlib
from matplotlib import dates
from datetime import datetime

import discord # discord bot API
from discord.commands import Option
import csv
import configparser
from datetime import datetime
import matplotlib.pyplot as plt

# the intents stuff is required for getting a list of members of a server
intents = discord.Intents.all()

client = discord.Bot()



# what the bot should do when it boots up
@client.event
async def on_ready():
    print("The bot is online and active")

    guild = discord.utils.get(client.guilds)
    print("{} is connected to the following guild: {}".format(client.user, guild.name))

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your waste")) # a fun discord status thing

# Slash command for accessing bot data
@client.slash_command(
    name='view_data',
    description='View Bot Data'
)
async def view_data(ctx, timespan: Option(str, "timespan", required = True)):

    # initializing three lists to store date time, trash level, trash count
    datetime_list = []
    trash_level = []
    trash_count = []

    try:
        with open("datafile.csv", "r") as datafile:
            trash_data = []
            datareader = csv.reader(datafile)
            #print(datareader)
            for row in datareader:
                datetime_list.append(datetime.strptime(row[1], '%d/%m/%y %H:%M:%S'))
                trash_level.append(row[1])
                trash_count.append(row[2])
                #print(trash_data)
            if(timespan == "level"):
                plt.plot(datetime_list, trash_level)
            else:
                plt.plot(datetime_list, trash_count)
            plt.savefig("plot.png")
            await ctx.respond((file=discord.File('plot.png')))
    except:
        await ctx.respond("Error, could not load the data!")





# Read the token and run the bot
token = ""
tokens_file = "token.txt"
token_list = configparser.ConfigParser()
token_list.read(tokens_file)
token_list = token_list["tokens"]
token = token_list["TTTbot"]
print("Starting bot")
client.run(token)
