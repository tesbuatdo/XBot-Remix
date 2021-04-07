from __future__ import unicode_literals
import os
from os import path
import ffmpeg
from typing import Union
from userbot.events import register
from userbot import bot, converter, callsmusic
from telethon.tl.types import DocumentAttributeAudio as Audio


def get_file_name(audio: Union[Audio]):
    return f'{audio.file_unique_id}.{audio.file_name.split(".")[-1] if not isinstance(audio) else "ogg"}'


@register(outgoing=True, pattern=r"^\.play")
async def xvcg(event):
    if event.fwd_from:
        return
    audio = await event.get_reply_message()
    if not (audio and (audio.media)):
        await event.edit("`Reply to any media`")
        return
    file_name = get_file_name(audio)
    file_path = await converter.convert(
            (await bot.download_media(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    await event.edit("Downloading Music....")
    if event.chat.id in callsmusic.pytgcalls.active_calls:
        await event.edit(f"Queued at position {await callsmusic.queues.put(event.chat.id, file_path=file_path)}!")
    else:
        callsmusic.pytgcalls.join_group_call(event.chat.id, file_path)
        await event.edit("Memutar Music...")

