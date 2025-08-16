# ---------------------------------------------------
# File Name: init.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Code Devil
# GitHub: https://github.com/Codedevil24/
# Telegram: https://t.me/Code_devil24
# YouTube: https://youtube.com/@Code_Devil
# Created: 2025-08-11
# Last Modified: 2025-08-16
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

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
    workers=20,  # Reduced to avoid resource overload
    parse_mode=ParseMode.MARKDOWN
)

pro = Client("ggbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING) if STRING else None
userrbot = Client("userrbot", api_id=API_ID, api_hash=API_HASH, session_string=DEFAULT_SESSION) if DEFAULT_SESSION else None

# Initialize Telethon client with exponential backoff retry
session_file = "telethon_session.session"
if os.path.exists(session_file):
    os.remove(session_file)  # Reset session to avoid nonce errors

max_retries = 5
backoff_factor = 2
for attempt in range(max_retries):
    try:
        telethon_client = TelegramClient('telethon_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
        logging.info(f"Telethon client started successfully on attempt {attempt + 1}")
        break
    except FloodWaitError as e:
        wait_time = min(e.seconds * (backoff_factor * attempt), 3600)  # Fixed syntax, cap at 1 hour
        if wait_time > 3600:
            logging.error(f"Excessive FloodWait ({wait_time} seconds). Consider refreshing BOT_TOKEN.")
        logging.warning(f"FloodWaitError: Waiting for {wait_time} seconds (attempt {attempt + 1}/{max_retries})...")
        time.sleep(wait_time)
    except AuthKeyError as e:
        logging.warning(f"AuthKeyError (nonce issue): {e}. Retrying {attempt + 1}/{max_retries}...")
        time.sleep(5 * (backoff_factor * attempt))
    except Exception as ex:
        logging.error(f"Error during Telethon start: {ex}")
        if attempt == max_retries - 1:
            raise

# MongoDB setup
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]

async def create_ttl_index():
    """Ensure the TTL index exists for the tokens collection."""
    await token.create_index("expires_at", expireAfterSeconds=0)

async def setup_database():
    """Set up MongoDB TTL index."""
    await create_ttl_index()
    logging.info("MongoDB TTL index created.")

# Global variables for bot info
BOT_ID = None
BOT_USERNAME = None
BOT_NAME = None
