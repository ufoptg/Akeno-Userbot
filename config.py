import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()
API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]
TELETHON_SESSION = os.environ["TELETHON_SESSION"]
FEDBAN_API_KEY = os.environ["FEDBAN_API_KEY"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
CMD_HANDLER = ["?"]
