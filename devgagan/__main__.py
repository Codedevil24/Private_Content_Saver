import nest_asyncio
from pyrogram import Client, idle
import asyncio
import importlib
import gc
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users
from aiojobs import create_scheduler
from devgagan import app, pro, userrbot, setup_database, telethon_client, BOT_ID, BOT_USERNAME, BOT_NAME

# Awake render container
from flask import Flask
import threading, os

app = Flask(__name__)

@app.route('/')
def ok():
    return 'OK', 200

def keep_alive():
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Daemon thread start – blocks nahi karega
threading.Thread(target=keep_alive, daemon=True).start()
#ending

# Enable nested event loops
nest_asyncio.apply()

# Function to schedule expiry checks
async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(3600)  # Check every hour
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
▶️ YouTube: https://youtube.com/@Code_Devil
🗓 Created: 2025-08-11
🔄 Last Modified: 2025-08-16
🛠 Version: 2.0.5
📜 License: MIT License
---------------------------------------------------
""")

    # Setup database and start clients
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

    # Start expiry check task
    asyncio.create_task(schedule_expiry_check())
    print("Auto removal started ...")

    # Keep the bot running
    await idle()  # Ensure the event loop stays alive

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(devggn_boot())  # Run the boot coroutine
    except KeyboardInterrupt:
        logging.info("Shutting down bot...")
        loop.run_until_complete(app.stop())
        if pro:
            loop.run_until_complete(pro.stop())
        if userrbot:
            loop.run_until_complete(userrbot.stop())
