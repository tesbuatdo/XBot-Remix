from os import path
import asyncio
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from userbot.events import register
from userbot import bot
from telethon.tl.types import DocumentAttributeAudio as Audio
from pytgcalls import PyTgCalls
pytgcalls = PyTgCalls(bot)
run = pytgcalls.run

async def convert(file_path: str) -> str:
    out = path.basename(file_path)
    out = out.split(".")
    out[-1] = "raw"
    out = ".".join(out)
    out = path.basename(out)
    out = path.join("raw_files", out)

    if path.isfile(out):
        return out

    proc = await asyncio.create_subprocess_shell(
        f"ffmpeg -y -i {file_path} -f s16le -ac 1 -ar 48000 -acodec pcm_s16le {out}",
        asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await proc.communicate()
    return out

@register(outgoing=True, pattern=r"^\.play")
async def vcg(event):
    if event.fwd_from:
        return
    ureply = await event.get_reply_message()
    if not (ureply and (ureply.media)):
        await event.edit("`Reply to any media`")
        return
    await event.edit("Downloading Music....")
    song = await event.client.download_media(ureply)
    await event.edit("Transcode...")
    file_path = convert(song)
    await event.edit("Memutar Music...")
    await pytgcalls.join_group_call(event.chat_id, file_path)
