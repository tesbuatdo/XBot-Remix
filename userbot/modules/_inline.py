from userbot.events import register
from userbot import bot, tgbot
from telethon import events, Button
rtext = """
🔥 XBOT REMIX USERBOT 🔥

  Running with telethon modules

• XBOT version: X01
• License: [Raphielscape](https://github.com/ximfine/XBot-Remix/blob/alpha/LICENSE)

Thanks for using repo
"""


@register(outgoing=True, pattern="!repo")
async def xrepo(repo):
    await tgbot.send_message(repo.chat_id, caption=rtext,
                             buttons=[[Button.url(text="GITHUB REPO",
                                                  url="https://github.com/ximfine/XBot-Remix")]])
