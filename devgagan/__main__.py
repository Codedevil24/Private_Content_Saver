import nest_asyncio
from pyrogram import Client, idle
import asyncio
import importlib
import gc
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users
from aiojobs import create_scheduler
from config import API_ID, API_HASH, BOT_TOKEN  # Assuming these are imported

# Enable nested event loops to prevent "Event loop is closed" errors
nest_asyncio.apply()

# Initialize Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to schedule expiry checks
async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(3600)  # Check every hour (3600 seconds)
        gc.collect()

async def devggn_boot():
    # Import all modules
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
🔄 Last Modified: 2025-08-11
🛠 Version: 2.0.5
📜 License: MIT License
---------------------------------------------------
""")

    # Start expiry check task
    asyncio.create_task(schedule_expiry_check())
    print("Auto removal started ...")

if __name__ == "__main__":
    app.run()  # Runs the bot, handles start, idle, and stop properly
