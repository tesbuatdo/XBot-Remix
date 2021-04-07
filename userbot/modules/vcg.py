from __future__ import unicode_literals
import youtube_dl
import asyncio
import time
import os
from pytgcalls import GroupCall

import ffmpeg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from telethon import TelegramClient
from telethon.events import NewMessage
from telethon import functions, types, events
from userbot.events import register
import requests, os ,re
import PIL
import cv2
import random
import numpy as np
from colour import Color
from telegraph import upload_file
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image, ImageOps, ImageDraw, ImageFont
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto


from userbot import bot

def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=1, ar='48000').overwrite_output().run() 
    os.remove(filename)

vc = GroupCall(bot, input_filename="input.raw", play_on_repeat=True)

# Arq Client
arq = ARQ(ARQ_API)

playing = False  # Tells if something is playing or not
chat_joined = False  # Tell if chat is joined or not

path = "./downloads/"

@register(outgoing=True, pattern=r"^\.play$")
async def vcg(event):
    if event.fwd_from:
        return
    ureply = await event.get_reply_message()
    if not (ureply and (ureply.media)):
        await event.reply("`Reply to any media`")
        return
    song = await bot.download_media(ureply, path, filename="song")
    await event.edit("Transcode...")
    transcode(song)
    await event.edit("Memutar Music...")
    
    
@register(outgoing=True, pattern=r"^\.joinvc$")
async def joinvc(event):
    global chat_joined
    try:
        if bot.chat_joined:
            await event.edit("__**Bot Is Already In Voice Chat.**__")
            return
        chat_id = event.chat.id
        await bot.vc.start(chat_id)
        bot.chat_joined = True
        await event.edit("__**Joined The Voice Chat.**__")
        await asyncio.sleep(10)
        await event.delete()


@register(outgoing=True, pattern=r"^\.leavevc$")
async def leavevc(event):
    global chat_joined
    if not bot.chat_joined:
        await event.edit("__**Already Out Of Voice Chat.**__")
        return
    bot.chat_joined = False
    await event.edit("__**Left The Voice Chat.**__")
    await asyncio.sleep(10)
    await event.delete()

