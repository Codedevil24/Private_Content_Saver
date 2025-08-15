
# ---------------------------------------------------
# File Name: __main__.py
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


import os
import importlib
from pyrogram import Client, idle
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users
from aiojobs import create_scheduler
import sys

# Add /app to sys.path if needed for module imports
sys.path.insert(0, '/app')

# Load environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")
LOG_GROUP = os.getenv("LOG_GROUP")
MONGO_DB = os.getenv("MONGO_DB")

# Initialize the Pyrogram client
app = Client(
    "Private_Content_Saver",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="devgagan.modules")  # Adjust if module structure differs
)

# Function to schedule expiry checks
async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(3600)  # Check every hour (changed from 60s for stability)

async def devggn_boot():
    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)
    
    print("""
---------------------------------------------------
📂 Bot Deployed successfully ...
📝 Description: A Pyrogram bot for downloading files from Telegram channels or groups 
                and uploading them back to Telegram.
👨‍💻 Author: Code Devil
🌐 GitHub: https://github.com/Codedevil24
📬 Telegram: https://t.me/Code_devil24
▶ YouTube: https://youtube.com/@Code_Devil
🗓 Created: 2025-08-11
🔄 Last Modified: 2025-08-15
🛠 Version: 2.0.5
📜 License: MIT License
---------------------------------------------------
""")

    print("Auto removal started ...")
    asyncio.create_task(schedule_expiry_check())  # Run scheduler in background

# Start the bot with Pyrogram's built-in event loop
if _name_ == "_main_":
    with app:
        app.run(devggn_boot())  # Pyrogram manages the event loop
    print("Bot stopped...")  # This will only run if the bot is stopped externally
