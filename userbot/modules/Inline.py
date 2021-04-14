from userbot import tgbot, bot
from telethon import Button, events
import logging
import random
import re

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



xrepo = ("Klik here", buttons=[[Button.url(text="GITHUB REPO",
                                                  url="https://github.com/ximfine/XBot-Remix")]])

@register(outgoing=True, pattern=r"^\.xrepo")
async def yardim(event):
    tgbotusername = BOT_USERNAME
    if tgbotusername and BOT_TOKEN:
        try:
            results = await event.client.inline_query(tgbotusername, xrepo)
        except BotInlineDisabledError:
            return await event.edit(
                "`Bot can't be used in inline mode.\nMake sure to turn on inline mode!`"
            )
        await results[0].click(
            event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
        )
        await event.delete()
    else:
        return await event.edit(
            "`The bot doesn't work! Please set the Bot Token and Username correctly.`"
            "\n`The module has been stopped.`"
        )
