from __future__ import unicode_literals
import os
from os import path
from pytgcalls import GroupCall
import ffmpeg
from typing import Union
from userbot.events import register
from userbot import bot, converter, callsmusic
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


def get_file_name(audio: Union[Audio]):
    return f'{audio.file_unique_id}.{audio.file_name.split(".")[-1] if not isinstance(audio) else "ogg"}'

vc = GroupCall(bot, input_filename="input.raw", play_on_repeat=True)

playing = False  # Tells if something is playing or not
chat_joined = False  # Tell if chat is joined or not


@register(outgoing=True, pattern=r"^\.play$")
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


@register(outgoing=True, pattern=r"^\.xplay$")
async def xvcg(event):
    if event.fwd_from:
        return
    audio = await event.get_reply_message()
    if not (audio and (audio.media)):
        await event.edit("`Reply to any media`")
        return
    await event.edit("Downloading Music....")
    file_name = get_file_name(audio)
    file_path = await converter.convert(
            (await event.client.download_media(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    
    if event.chat.id in callsmusic.pytgcalls.active_calls:
        await event.edit(f"Queued at position {await callsmusic.queues.put(event.chat.id, file_path=file_path)}!")
    else:
        callsmusic.pytgcalls.join_group_call(event.chat.id, file_path)
        await event.edit("Memutar Music...")



@register(outgoing=True, pattern="^\.jvc")
async def joinvc(event):
    await vc.start(event.chat.id)
    await event.edit("__**Joined The Voice Chat.**__")
