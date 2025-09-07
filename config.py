# Code Devil
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = int(getenv("API_ID", "23677130"))
API_HASH = getenv("API_HASH", "805dcfa1dca9bf80f70a571bf6deb7c0")
BOT_TOKEN = getenv("BOT_TOKEN", "8438851683:AAFdB7d9_k4HK0ESkesaYRg0MoIEnXVpMpk")
OWNER_ID = list(map(int, getenv("OWNER_ID", "6859104243").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://devv54123_db_user:qOzHhthxTdTVpU3j@cluster0.m3egcli.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = getenv("LOG_GROUP", "-1002828779986")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1001579030541"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "30"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500"))
WEBSITE_URL = getenv("WEBSITE_URL", "gplink.com")
AD_API = getenv("AD_API", "e1b77a06fabdc3b60c575020fc9382fd33bedc39")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", None)
DEFAULT_SESSION = getenv("DEFAUL_SESSION", None)  # added old method of invite link joining
INSTA_COOKIES = getenv("INSTA_COOKIES", None)
