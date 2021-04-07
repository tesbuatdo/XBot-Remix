from __future__ import unicode_literals
import asyncio
import os
from pytgcalls import GroupCall

import ffmpeg
from userbot.events import register
import os


from userbot import bot


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw",
        format='s16le',
        acodec='pcm_s16le',
        ac=1,
        ar='48000').overwrite_output().run()
    os.remove(filename)


vc = GroupCall(bot, input_filename="input.raw", play_on_repeat=True)

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
    await asyncio.sleep(600)
    os.remove(input.raw)

global chat_joined


@register(outgoing=True, pattern=r"^\.joinvc$")
async def joinvc(event):
    if event.fwd_from:
        return
    chat_id = event.chat.id
    if bot.chat_joined:
        await event.edit("__**Bot Is Already In Voice Chat.**__")
        return
    await bot.vc.start(chat_id)
    bot.chat_joined = True
    await event.edit("__**Joined The Voice Chat.**__")
