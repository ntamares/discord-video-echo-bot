import asyncio, discord, os, logging
from dotenv import load_dotenv
from discord.ext import commands
from services.downloader import download_video
from utils.link_parser import extract_supported_url
from utils.channel_id_parser import parse_allowed_channels
from utils.logger import setup_activity_logging, setup_error_logging

load_dotenv()
error_logger = setup_error_logging()
activity_logger = setup_activity_logging()
app_logger = logging.getLogger(__name__)

TOKEN = os.getenv("DISCORD_TOKEN")
ALLOWED_CHANNELS_RAW = os.getenv("ALLOWED_CHANNELS")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

if not ALLOWED_CHANNELS_RAW:
    raise ValueError("ALLOWED_CHANNELS environment variable is not set")

ALLOWED_CHANNELS = parse_allowed_channels(ALLOWED_CHANNELS_RAW)
if not ALLOWED_CHANNELS:
    raise ValueError("ALLOWED_CHANNELS environment variable did not contain valid channel IDs")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix = "$",
    intents=intents
)

@bot.event
async def on_ready():
    app_logger.info("Logged in as %s", bot.user)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.channel.id not in ALLOWED_CHANNELS:
        return
    
    url = extract_supported_url(message.content)

    if not url:
        return

    file_path: str | None = None
    
    try:
        file_path = await asyncio.to_thread(download_video, url)
        file_size = os.path.getsize(file_path)
        user_tag = str(message.author)
        user_id = message.author.id
        channel_id = message.channel.id
        guild_id = message.guild.id if message.guild else None

        activity_logger.info(
            "download_success url=%s file_size_bytes=%s message_id=%s user_tag=%s user_id=%s channel_id=%s guild_id=%s",
            url,
            file_size,
            message.id,
            user_tag,
            user_id,
            channel_id,
            guild_id,
        )

        await message.reply(
            file=discord.File(file_path),
            mention_author=False
        )

        activity_logger.info(
            "upload_success url=%s file_size_bytes=%s message_id=%s user_tag=%s user_id=%s channel_id=%s guild_id=%s",
            url,
            file_size,
            message.id,
            user_tag,
            user_id,
            channel_id,
            guild_id,
        )
        
    except ValueError as exc:
        error_logger.error(
            "Handled failure message_id=%s url=%s error=%s",
            message.id,
            url,
            str(exc),
        )
    except Exception:
        error_logger.exception(
            "Unexpected failure while processing message_id=%s url=%s",
            message.id,
            url,
        )
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

    await bot.process_commands(message)

bot.run(TOKEN)