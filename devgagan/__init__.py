# ---------------------------------------------------
# File Name: __init__.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Code Devil
# GitHub: https://github.com/Codedevil24/
# Telegram: https://t.me/Code_devil24
# YouTube: https://youtube.com/@Code_Devil
# Created: 2025-08-11
# Last Modified: 2025-08-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

import asyncio
import logging
import time
import os
import nest_asyncio
from pyrogram import Client
from pyrogram.enums import ParseMode 
from telethon import TelegramClient
from telethon.errors import FloodWaitError, AuthKeyError
from motor.motor_asyncio import AsyncIOMotorClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING, MONGO_DB, DEFAULT_SESSION

# Enable nested event loops to prevent "Event loop is closed" errors
nest_asyncio.apply()

# Set up logging
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

botStartTime = time.time()

# Initialize Pyrogram clients
app = Client(
    "pyrobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,
    parse_mode=ParseMode.MARKDOWN
)

pro = Client("ggbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING) if STRING else None
userrbot = Client("userrbot", api_id=API_ID, api_hash=API_HASH, session_string=DEFAULT_SESSION) if DEFAULT_SESSION else None

# Initialize Telethon client with retry logic
session_file = "telethon_session.session"
if os.path.exists(session_file):
    os.remove(session_file)  # Reset session to avoid nonce errors

for attempt in range(3):  # Retry up to 3 times
    try:
        telethon_client = TelegramClient('telethon_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
        break  # Success, exit loop
    except FloodWaitError as e:
        logging.info(f"FloodWaitError: Waiting for {e.seconds} seconds...")
        time.sleep(e.seconds + 10)
    except AuthKeyError as e:
        logging.info(f"AuthKeyError (nonce issue): {e}. Retrying {attempt + 1}/3...")
        time.sleep(5)
    except Exception as ex:
        logging.error(f"Error during Telethon start: {ex}")
        if attempt == 2:
            raise  # Raise on last attempt
        time.sleep(5)

# MongoDB setup
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]  # Your database
token = tdb["tokens"]  # Your tokens collection

async def create_ttl_index():
    """Ensure the TTL index exists for the tokens collection."""
    await token.create_index("expires_at", expireAfterSeconds=0)

async def setup_database():
    """Set up MongoDB TTL index."""
    await create_ttl_index()
    logging.info("MongoDB TTL index created.")

async def restrict_bot():
    """Initialize bot and clients."""
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await setup_database()
    await app.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name
    
    if pro:
        await pro.start()
    if userrbot:
        await userrbot.start()
