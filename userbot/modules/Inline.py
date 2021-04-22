import logging
import time
import speedtest
import heroku3
import aiohttp
import math
import asyncio
from telethon import Button, events
from datetime import datetime
from userbot import tgbot, StartTime, HEROKU_APP_NAME, HEROKU_API_KEY

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.WARNING)

rtext = """
🔥 **XBOT REMIX USERBOT** 🔥

   `Running with telethon modules`

**• XBOT version:** X-01
**• Branch:** sql-extended
**• License:** [Raphielscape](https://github.com/ximfine/XBot-Remix/blob/alpha/LICENSE)

__Klik button below to use my repo__
"""


@tgbot.on(events.NewMessage(pattern="!repo"))
async def xrepo(repo):
    await tgbot.send_message(repo.chat_id, rtext,
                             buttons=[[Button.url(text="GITHUB REPO",
                                                  url="https://github.com/ximfine/XBot-Remix")]])


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


@tgbot.on(events.NewMessage(pattern="!speed"))
async def spd(event):
    asu = await event.reply("`Test Speed Internet connection` ⚡")
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
    response = s.results.share()
    speedtest_image = response
    output = (f"**SpeedTest** completed in {ms}ms\n\n"
              f"`•Download: {speed_convert(download_speed)}\n`"
              f"`•Upload: {speed_convert(upload_speed)}\n`"
              f"`•Ping: {ping_time}\n`"
              f"`•ISP: {i_s_p}\n`"
              f"`•ISP Rating: {i_s_p_rating}\n\n`"
              "**POWERED BY XBOT REMIX 🔥**")
    await asu.delete()
    await tgbot.send_file(
        event.chat_id,
        speedtest_image,
        caption=output,
        force_document=False,
        allow_cache=False
    )


@tgbot.on(events.NewMessage(pattern="!ping"))
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.reply("`Pinging....`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await tgbot.send_message(pong.chat_id, f"**PONG!! 🍭**\n**Pinger** : %sms\n**Bot Uptime** : {uptime}🕛" % (duration))


heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


@tgbot.on(events.NewMessage(pattern="!usage"))
async def dyno_usage(dyno):
    """
        Get your account Dyno Usage
    """
    x = await dyno.reply("`Getting Information...`")
    useragent = (
        'Mozilla/5.0 (Linux; Android 10; SM-G975F) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/81.0.4044.117 Mobile Safari/537.36'
    )
    user_id = Heroku.account().id
    headers = {
        'User-Agent': useragent,
        'Authorization': f'Bearer {HEROKU_API_KEY}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    async with aiohttp.ClientSession() as session:
        async with session.get(heroku_api + path, headers=headers) as r:
            if r.status != 200:
                await tgbo.send_message(
                    dyno.chat_id,
                    f"`{r.reason}`",
                    reply_to=dyno.id
                )
                await x.edit("`Can't get information...`")
                return False
            result = await r.json()
            quota = result['account_quota']
            quota_used = result['quota_used']

            """ - User Quota Limit and Used - """
            remaining_quota = quota - quota_used
            percentage = math.floor(remaining_quota / quota * 100)
            minutes_remaining = remaining_quota / 60
            hours = math.floor(minutes_remaining / 60)
            minutes = math.floor(minutes_remaining % 60)

            """ - User App Used Quota - """
            Apps = result['apps']
            for apps in Apps:
                if apps.get('app_uuid') == app.id:
                    AppQuotaUsed = apps.get('quota_used') / 60
                    AppPercentage = math.floor(
                        apps.get('quota_used') * 100 / quota)
                    break
            else:
                AppQuotaUsed = 0
                AppPercentage = 0

            AppHours = math.floor(AppQuotaUsed / 60)
            AppMinutes = math.floor(AppQuotaUsed % 60)

            await x.edit(
                "**Dyno Usage**:\n\n╭━━━━━━━━━━━━━━━━━━━━╮\n"
                f" ❁ **Penggunaan Dyno** **{app.name}**:\n"
                f"    •**{AppHours} jam - "
                f"{AppMinutes} menit - {AppPercentage}%**"
                "\n  ≪━━◈≪━─━─࿇─━─━≫◈━━≫\n"
                " ❁ **Sisa Dyno Bulan Ini**:\n"
                f"    •**{hours} jam - {minutes} menit  "
                f"- {percentage}%**\n"
                "╰━━━━━━━━━━━━━━━━━━━━╯"
            )
            await asyncio.sleep(20)
            await x.delete()
            return True
