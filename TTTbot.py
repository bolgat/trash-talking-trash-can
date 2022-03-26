import discord # discord bot API
from discord.commands import Option
import configparser
from datetime import datetime

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
    
    try:
        with open("datafile.txt", "rb") as datafile:
            trash_data = pickle.load(datafile)
            await ctx.respond(f"**You asked for data for the past:**\n{trash_data}")
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
