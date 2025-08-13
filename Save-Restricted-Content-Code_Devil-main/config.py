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

API_ID = int(getenv("API_ID", "23057509"))
API_HASH = getenv("API_HASH", "a1ba4eb481c7333fc8822de292e46f5e")
BOT_TOKEN = getenv("BOT_TOKEN", "8357607201:AAHlT9rp4k0pDHwrjqf_wif5lede60t5AUI")
OWNER_ID = list(map(int, getenv("OWNER_ID", "5083822493").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://devv54123:sz7hqWLr9cNzN5JG@cluster0.ahus5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = getenv("LOG_GROUP", "-1002828779986")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1001579030541"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "30"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500"))
WEBSITE_URL = getenv("WEBSITE_URL", "gplink.com")
AD_API = getenv("AD_API", "e1b77a06fabdc3b60c575020fc9382fd33bedc39")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", YTUB_COOKIES)
DEFAULT_SESSION = getenv("DEFAUL_SESSION", None)  # added old method of invite link joining
INSTA_COOKIES = getenv("INSTA_COOKIES", INST_COOKIES)
