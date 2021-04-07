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


@register(outgoing=True, pattern=r"^\.play$")
async def vcg(event):
    if event.fwd_from:
        return
    ureply = await event.get_reply_message()
    if not (ureply and (ureply.media)):
        await event.edit("`Reply to any media`")
        return
    song = await event.client.download_media(ureply)
    await event.edit("Transcode...")
    transcode(song)
    await event.edit("Memutar Music...")
    await asyncio.sleep(600)
    os.remove(input.raw)


@register(outgoing=True, pattern=r"^\.joinvc$")
async def joinvc(event):
    chat_id = event.chat.id
    await bot.vc.start(chat_id)
    bot.chat_joined = True
    await event.edit("__**Joined The Voice Chat.**__")
