import asyncio
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from services.downloader import download_video
from utils.link_parser import extract_supported_url

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ALLOWED_CHANNELS = {
    547910426994933793,
    779579821209550859,
    445058358983131143,
    898427904801783878,
    533888115186728961,
    1102690101408038942,
    1117958655829082205,
    707120335882813480,
    721222588688236604,
    1234185445806440509,
}

if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

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
    
    if message.channel.id not in ALLOWED_CHANNELS:
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