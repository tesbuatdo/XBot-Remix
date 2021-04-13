# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway (yes, Internet). """

import speedtest
import time
from datetime import datetime
from userbot import StartTime, bot, CMD_HELP
from userbot.events import register


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


def xconvert(speed):
    return round(int(speed) / 1048576, 2)

@register(outgoing=True, pattern="^\\.speed$")
async def speedtest(event):
    if event.fwd_from:
        return
    await event.edit("`Test Internet Speed Connection..`⚡")
    speed = speedtest.Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()
    replymsg = "SpeedTest Results:"
    speedtest_image = speed.results.share()
    output = replymsg += f"\nDownload: `{xconvert(result['download'])}Mb/s`\nUpload: `{xconvert(result['upload'])}Mb/s`\nPing: `{result['ping']}`"
    await event.reply_photo(
        event.chat_id,
        photo=speedtest_image,
        caption=output,
        force_document=False,
    )
    


@register(outgoing=True, pattern="^.ping$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("`Pinging....`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**PONG!! 🍭**\n**Pinger** : %sms\n**Bot Uptime** : {uptime}🕛" % (duration))


@register(outgoing=True, pattern="^.pong$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`gass!`")
    end = datetime.now()
    duration = (end - start).microseconds / 9000
    await pong.edit("`Ping!\n%sms`" % (duration))


@register(outgoing=True, pattern="^.pink$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`Croots!`")
    end = datetime.now()
    duration = (end - start).microseconds / 9000
    await pong.edit("**CROOTSS!\n%sms**" % (duration))


CMD_HELP.update(
    {"ping": "`.ping`\
    \nUsage: Shows how long it takes to ping your bot.\
    \n\n`.speed`\
    \nUsage: Does a speedtest and shows the results.\
    \n\n`.pong`\
    \nUsage: Shows how long it takes to ping your bot."
     })
