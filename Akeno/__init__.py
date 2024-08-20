import asyncio
import logging
import os
import random
import re
import string
import time
from datetime import datetime as dt
from inspect import getfullargspec
from os import path
from platform import python_version
from random import choice

import aiohttp
import pyrogram
from aiohttp import ClientSession
from pyrogram import Client
from pyrogram import __version__ as pyrogram_version
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.raw.all import layer
from pyrogram.types import *
from pytgcalls import GroupCallFactory
from telethon import TelegramClient

from Akeno.utils.logger import LOGS
from config import API_HASH, API_ID, SESSION, TELETHON_SESSION

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

StartTime = time.time()
START_TIME = dt.now()
CMD_HELP = {}
clients = []
ids = []
act = []
db = {}

SUDOERS = filters.user()

aiohttpsession = ClientSession()

__version__ = {
# Pyrogram Client
    "pyrogram": pyrogram_version,
    "python": python_version(),
}

# Pyrogram Client
client = Client(
    "one",
    app_version="latest",
    device_model="Akeno",
    system_version="Linux",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
    plugins=dict(root="Akeno.plugins"),
)
if not hasattr(client, "group_call"):
    setattr(client, "group_call", GroupCallFactory(client).get_group_call())

clients.append(client)

# Telethon Client
telethon_client = TelegramClient(
    TELETHON_SESSION,  # You need to specify this in your config file
    API_ID,
    API_HASH
)
clients.append(telethon_client)

# Starting the clients
async def start_clients():
    await client.start()
    await telethon_client.start()
    logger.info("Both clients have been started successfully.")

loop = asyncio.get_event_loop()
loop.run_until_complete(start_clients())
