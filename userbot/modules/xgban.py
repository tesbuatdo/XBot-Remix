# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from telethon import events


from userbot import bot
from userbot.events import register


DEVLIST = 1560233393


@register(outgoing=True, pattern=r"^\.xungban(?: |$)(.*)")
async def _(e):
    xx = await e.edit("`UnGbanning...`")
    if e.is_private:
        userid = (await e.get_chat()).id
    elif e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
    elif e.pattern_match.group(1):
        if (e.pattern_match.group(1)).isdigit():
            try:
                userid = (await e.client.get_entity(int(e.pattern_match.group(1)))).id
            except ValueError as err:
                return await xx.edit(f"{str(err)}", time=5)
        else:
            try:
                userid = (await e.client.get_entity(str(e.pattern_match.group(1)))).id
            except ValueError as err:
                return await xx.edit(f"{str(err)}", time=5)
    else:
        return await xx.edit("`Reply to some msg or add their id.`", time=5)
    name = (await e.client.get_entity(userid)).first_name
    chats = 0

    async for ggban in e.client.iter_dialogs():
        if ggban.is_group or ggban.is_channel:
            try:
                await e.client.edit_permissions(ggban.id, userid, view_messages=True)
                chats += 1
            except BaseException:
                pass
    ungban(userid)
    await xx.edit(
        f"`Ungbanned` [{name}](tg://user?id={userid}) `in {chats} chats.\nRemoved from gbanwatch.`",
    )


@register(outgoing=True, pattern=r"^\.xgban(?: |$)(.*)")
async def _(e):
    xx = await e.edit("`Gbanning...`")
    if e.is_private:
        userid = (await e.get_chat()).id
    elif e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
    elif e.pattern_match.group(1):
        if (e.pattern_match.group(1)).isdigit():
            try:
                userid = (await e.client.get_entity(int(e.pattern_match.group(1)))).id
            except ValueError as err:
                return await xx.edit(f"{str(err)}", time=5)
        else:
            try:
                userid = (await e.client.get_entity(str(e.pattern_match.group(1)))).id
            except ValueError as err:
                return await xx.edit(f"{str(err)}", time=5)
    else:
        return await xx.edit("`Reply to some msg or add their id.`", tome=5)
    name = (await e.client.get_entity(userid)).first_name
    chats = 0
    if str(userid) in DEVLIST:
        return await xx.edit("`I can't gban my Developers.`", time=3)

    async for ggban in e.client.iter_dialogs():
        if ggban.is_group or ggban.is_channel:
            try:
                await e.client.edit_permissions(ggban.id, userid, view_messages=False)
                chats += 1
            except BaseException:
                pass
    gban(userid)
    await xx.edit(
        f"`Gbanned` [{name}](tg://user?id={userid}) `in {chats} chats.\nAdded to gbanwatch.`",
    )


@register(outgoing=True, pattern=r"^\.gcast(?: |$)(.*)")
async def gcast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`Give some text to Globally Broadcast`")
    tt = event.text
    msg = tt[6:]
    kk = await event.edit("`Globally Broadcasting Msg...`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"Done in {done} chats, error in {er} chat(s)")


@register(outgoing=True, pattern=r"^\.gucast(?: |$)(.*)")
async def gucast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`Give some text to Globally Broadcast`")
    tt = event.text
    msg = tt[7:]
    kk = await event.edit("`Globally Broadcasting Msg...`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"Done in {done} chats, error in {er} chat(s)")


@bot.on(events.ChatAction)
async def _(e):
    if e.user_joined or e.added_by:
        user = await e.get_user()
        chat = await e.get_chat()
        if chat.admin_rights:
            try:
                await e.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                gban_watch = f"`Gbanned User` [{user.first_name}](tg://user?id={user.id}) `Spotted\n"
                gban_watch += f"Banned Successfully`"
                await e.reply(gban_watch)
            except BaseException:
                pass
