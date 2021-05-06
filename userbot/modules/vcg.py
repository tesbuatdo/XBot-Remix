import json
from json.decoder import JSONDecodeError

from userbot import bot
from userbot.events import register
from aiohttp import web
from aiohttp.http_websocket import WSMsgType

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.phone import (
    GetGroupCallRequest,
    JoinGroupCallRequest,
)
from telethon.tl.types import DataJSON


@register(outgoing=True, pattern=r"^\.joinvc")
async def join_call(data):
    try:
        chat = await get_entity(data.chat_id)
    except ValueError:
        stree = (await bot.get_me()).first_name
        return await bot.send_message(
            data.chat_id, f"`Please add {stree} in this group.`"
        )
    except Exception as ex:
        return await bot.send_message(data.chat_id, "`" + str(ex) + "`")
    try:
        full_chat = await bot(GetFullChannelRequest(chat))
    except ValueError:
        stree = (await bot.get_me()).first_name
        return await bot.send_message(
            data.chat_id, f"`Please add {stree} in this group.`"
        )
    except Exception as ex:
        return await bot.send_message(data.chat_id, "`" + str(ex) + "`")
    try:
        call = await bot(GetGroupCallRequest(full_chat.full_chat.call))
    except BaseException:
        call = None
    if not call:
        return await bot.send_message(
            data.chat_id,
            "`I can't access voice chat.`",
        )

    try:
        result = await data.client(
            JoinGroupCallRequest(
                call=call.call,
                muted=False,
                join_as="me",
                params=DataJSON(
                    data=json.dumps(
                        {
                            "ufrag": data["ufrag"],
                            "pwd": data["pwd"],
                            "fingerprints": [
                                {
                                    "hash": data["hash"],
                                    "setup": data["setup"],
                                    "fingerprint": data["fingerprint"],
                                },
                            ],
                            "ssrc": data["source"],
                        },
                    ),
                ),
            ),
        )
        await bot.send_message(
            data.chat_id, f"`Joined Voice Chat in {(await bot.get_entity(data.chat_id)).title}`",
        )
    except Exception as ex:
        return await bot.send_message(data.chat_id, "`" + str(ex) + "`")

    transport = json.loads(result.updates[0].call.params.data)["transport"]

    return {
        "_": "get_join",
        "data": {
            "chat_id": data["chat"]["id"],
            "transport": {
                "ufrag": transport["ufrag"],
                "pwd": transport["pwd"],
                "fingerprints": transport["fingerprints"],
                "candidates": transport["candidates"],
            },
        },
    }


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
            except JSONDecodeError:
                await ws.close()
                break

            response = None
            if data["_"] == "join":
                response = await join_call(data["data"])

            #                if data["_"] == "leave":
            #                    response = await leave_vc(data["data"])

            if response is not None:
                await ws.send_json(response)

    return ws
