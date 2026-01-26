from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
DB = os.getenv("DB")
DEV = os.getenv("DEV")
GUILD_ID = int(os.getenv("GUILD_ID"))

# set in env.py
CHANNELS = []
