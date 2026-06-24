import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from utils.link_parser import contains_supported_link

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID_RAW = os.getenv("BOT_TESTING_CHANNEL_ID")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

if not CHANNEL_ID_RAW:
    raise ValueError("BOT_TESTING_CHANNEL_ID environment variable is not set")

try:
    channel_id = int(CHANNEL_ID_RAW)
except ValueError:
    raise ValueError("BOT_TESTING_CHANNEL_ID must be an integer")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix = "$",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):

    if message.author.bot:
        return
    
    # TODO remove once done testing
    if message.channel.id == channel_id:
        if contains_supported_link(message.content):
            print("Supported link detected")
            await message.channel.send("Supported link was detected")
        else:
            print("Domain not supported")
            await message.channel.send("Domain not supported")

    await bot.process_commands(message)

bot.run(TOKEN)