
from utils import *

import discord # discord bot API
from discord.commands import Option
import pathlib
import os
import configparser
from datetime import datetime
from constants import *         # relevant constants for our bot

# the intents stuff is required for getting a list of members of a server
intents = discord.Intents.all()

client = discord.Bot()
logging = get_bot_logger()

# what the bot should do when it boots up
@client.event
async def on_ready():
    logging.info("The bot is online and active")
    logging.info("bot name: {}".format(client.user))

    guild = discord.utils.get(client.guilds)
    logging.info("{} is connected to the following guild: {}".format(client.user, guild.name))

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your documentation")) # a fun discord status thing

@client.slash_command(
    name='review',
    description='Create a Thread to Review a Confluence Page'
)
async def review(ctx, confpage: Option(str, "Link to a Confluence page", required = True)):
    spl_page = confpage.split('/')
    title = spl_page[-1].replace('+',' ')
    response = await ctx.respond(f"**Request for Review:**\n{confpage}")
    message = await response.original_message()
    await message.create_thread(name=title)

token = ""
tokens_file = "token.txt"
token_list = configparser.ConfigParser()

token_list.read(tokens_file)
token_list = token_list["tokens"]
token = token_list["TTTbot"]
logging.info("Starting bot")
logging.info("Time: {}".format(datetime.now()))
client.run(token)
