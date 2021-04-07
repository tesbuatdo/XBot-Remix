from __future__ import unicode_literals
import os
from os import path
import ffmpeg
from pytgcalls import GroupCall
from Python_ARQ import ARQ
from userbot.events import register
from userbot import bot
from telethon.tl.types import DocumentAttributeAudio as Audio


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw",
        format='s16le',
        acodec='pcm_s16le',
        ac=1,
        ar='48000').overwrite_output().run()
    os.remove(filename)

    return text[offset:offset + length]

ARQ_API = "http://35.240.133.234:8000"

arq = ARQ(ARQ_API)
vc = GroupCall(bot, input_filename="input.raw", play_on_repeat=True)

playing = False  # Tells if something is playing or not
chat_joined = False  # Tell if chat is joined or not


@register(outgoing=True, pattern=r"^\.play")
async def vcg(event):
    if event.fwd_from:
        return
    global playing
    ureply = await event.get_reply_message()
    if not (ureply and (ureply.media)):
        await event.edit("`Reply to any media`")
        return
    await event.edit("Downloading Music....")
    song = await event.client.download_media(ureply)
    await event.edit("Transcode...")
    transcode(song)
    playing = False  # pylint:disable=E0602
    await event.edit("Memutar Music...")
