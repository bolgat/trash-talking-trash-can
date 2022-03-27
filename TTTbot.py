import discord # discord bot API
import csv
import configparser
from datetime import datetime
import matplotlib.pyplot as plt

# the intents stuff is required for getting a list of members of a server
intents = discord.Intents.all()

client = discord.Client()

# what the bot should do when it boots up
@client.event
async def on_ready():
    print("The bot is online and active")

    guild = discord.utils.get(client.guilds)
    print("{} is connected to the following guild: {}".format(client.user, guild.name))

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your waste")) # a fun discord status thing

# Slash command for accessing bot data
@client.event
async def on_message(message):

    # initializing three lists to store date time, trash level, trash count
    datetime_list = []
    trash_level = []
    trash_count = []

#try:
    if(message.content.startswith("!plot")):
        with open("datafile.csv", "r") as datafile:
            trash_data = []
            datareader = csv.reader(datafile)
            #print(datareader)
            for row in datareader:
                datetime_list.append(datetime.strptime(row[0][:19], '%Y-%m-%d %H:%M:%S%f'))
                trash_level.append(float(row[1]))
                trash_count.append(int(row[2]))
                #print(trash_data)
            if(message.content.find("level") != -1):
                plt.plot(datetime_list, trash_level)
                plt.ylim([0,1.4])
                plt.title("Trash Level vs. Time")
            else:
                plt.plot(datetime_list, trash_count)
                plt.title("Cumulative Trash Count vs. Time")
            plt.savefig("plot.png")
            plt.cla()
            with open("plot.png", "rb") as fh:
                f = discord.File(fh, filename="plot.png")
            await message.channel.send(file=f)
    #except:
    #    await message.channel.send("Error, could not load the data!")


# Read the token and run the bot
token = ""
tokens_file = "token.txt"
token_list = configparser.ConfigParser()
token_list.read(tokens_file)
token_list = token_list["tokens"]
token = token_list["TTTbot"]
print("Starting bot")
client.run(token)
