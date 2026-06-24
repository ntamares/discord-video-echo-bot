import asyncio
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from services.downloader import download_video
from utils.link_parser import extract_supported_url

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# CHANNEL_ID_RAW = os.getenv("BOT_TESTING_CHANNEL_ID")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

# if not CHANNEL_ID_RAW:
#     raise ValueError("BOT_TESTING_CHANNEL_ID environment variable is not set")

# try:
#     CHANNEL_ID = int(CHANNEL_ID_RAW)
# except ValueError:
#     raise ValueError("BOT_TESTING_CHANNEL_ID must be an integer")

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
    
    url = extract_supported_url(message.content)

    #TODO better/more accurate logging

    if extract_supported_url(message.content) and url:        
        try:
            print("Downloading video")
            file_path = await asyncio.to_thread(download_video, url)

            await message.reply(
                file=discord.File(file_path),
                mention_author=False
            )

            os.remove(file_path)

        except Exception as e:
            await message.channel.send(f"Download failed: {e}")
    else:
        print("Domain not supported")

    await bot.process_commands(message)

bot.run(TOKEN)