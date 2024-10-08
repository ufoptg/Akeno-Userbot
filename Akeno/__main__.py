#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2020-2023 (c) Randy W @xtdevs, @xtsea
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import importlib
import logging
import sys
from contextlib import closing, suppress

import aiohttp
from pyrogram import idle
from pyrogram.errors import *
from uvloop import install

from Akeno import aiohttpsession, clients
from Akeno.utils.database import db
from Akeno.utils.logger import LOGS

import dns.resolver
import socket

logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
loop = asyncio.get_event_loop()

def custom_resolver(hostname):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["8.8.8.8", "8.8.4.4"]  # Using Google's DNS servers
    answers = resolver.resolve(hostname, "A")
    return answers[0].address


original_getaddrinfo = socket.getaddrinfo


def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    try:
        ip = custom_resolver(host)
        return [(socket.AF_INET, socket.SOCK_STREAM, proto, "", (ip, port))]
    except Exception as e:
        return original_getaddrinfo(host, port, family, type, proto, flags)


socket.getaddrinfo = custom_getaddrinfo

async def main():
    try:
        await db.connect()
        for cli in clients:
            try:
                await cli.start()
                ex = await cli.get_me()
                LOGS.info(f"Started {ex.first_name} - {type(cli).__name__}")
                await cli.send_message("me", "Starting Akeno Userbot")
                try:
                    await cli.join_chat("RendyProjects")
                except UserIsBlocked:
                    LOGS.info("You have been blocked. Please support @xtdevs")
            except SessionExpired as e:
                LOGS.info(f"Session expired for {type(cli).__name__}: {e}")
                sys.exit(1)
            except ApiIdInvalid as e:
                LOGS.info(f"Invalid API ID for {type(cli).__name__}: {e}")
                sys.exit(1)
            except UserDeactivated as e:
                LOGS.info(f"User deactivated for {type(cli).__name__}: {e}")
                sys.exit(1)
            except AuthKeyDuplicated as e:
                LOGS.info(f"Duplicate auth key for {type(cli).__name__}: {e}")
                sys.exit(1)
            except Exception as e:
                LOGS.info(f"Error starting {type(cli).__name__}: {e}")

        await idle()
    except Exception as e:
        LOGS.info(f"Error in main: {e}")
    finally:
        await asyncio.gather(
            aiohttpsession.close()
        )

        for task in asyncio.all_tasks():
            task.cancel()
        LOGS.info("All tasks completed successfully!")

if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(asyncio.exceptions.CancelledError):
            loop.run_until_complete(main())
        loop.run_until_complete(asyncio.sleep(3.0))
