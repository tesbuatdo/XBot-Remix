from random import randint
from time import sleep
from os import execl
import asyncio
import sys
import os
import io
import sys
from telethon import events, Button
from userbot import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, CMD_HELP, bot, tgbot
from userbot.events import register
from userbot.utils import time_formatter
import urllib
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image

rtext = """
🔥 XBOT REMIX USERBOT 🔥

  Running with telethon modules,

• XBOT version: X01
• License: [Raphielscape](https://github.com/ximfine/XBot-Remix/blob/alpha/LICENSE)

Thanks for using repo
"""


@register(outgoing=True, pattern="!repo")
async def xrepo(repo):
    await tgbot.send_message(repo.chat_id, caption=rtext,
                             buttons=[[Button.url(text="GITHUB REPO",
                                               url="https://github.com/ximfine/XBot-Remix")]])
