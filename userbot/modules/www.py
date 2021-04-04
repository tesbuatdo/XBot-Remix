# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway (yes, Internet). """


import time
import io
import speedtest
from datetime import datetime
from speedtest import Speedtest
from userbot import CMD_HELP, StartTime, bot
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


@register(outgoing=True, pattern="^.speed$")
async def speedtst(spd):
    """ For .speed command, use SpeedTest to check server speeds. """
    await spd.edit("`Running high speed test . . .`")
    test = Speedtest()

    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()

    await spd.edit("`"
                   "Started at "
                   f"{result['timestamp']} \n\n"
                   "Download "
                   f"{speed_convert(result['download'])} \n"
                   "Upload "
                   f"{speed_convert(result['upload'])} \n"
                   "Ping "
                   f"{result['ping']} \n"
                   "ISP "
                   f"{result['client']['isp']}"
                   "`")


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


@register(outgoing=True, pattern="^.speed$")
async def speedtst(event):
    await event.edit("`Test Speed Internet connection.`🔥")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000

    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")

    reply_msg_id = event.message.id
    if event.reply_to_msg_id:
        reply_msg_id = event.reply_to_msg_id
    try:    
        response = s.results.share()
        speedtest_image = response

        await bot.send_file(
            event.chat_id,
            speedtest_image,
            caption="""**SpeedTest** completed in {} seconds\nDownload: {}\nUpload: {}\nPing: {}\nInternet Service Provider: {}\nISP Rating: {}""".format(ms, convert_from_bytes(download_speed), convert_from_bytes(upload_speed), ping_time, i_s_p, i_s_p_rating),
            force_document=False,   
            reply_to=reply_msg_id,        
            allow_cache=False
        )
        await event.delete()

def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {
        0: "",
        1: "kilobytes",
        2: "megabytes",
        3: "gigabytes",
        4: "terabytes"
    }
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"
