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
    LeaveGroupCallRequest,
)
from telethon.tl.types import DataJSON

@register(outgoing=True, pattern=r"^\.joinvc")
async def join_call(data):
        try:
            chat = await get_entity(data["chat"])
        except ValueError:
            stree = (await bot.get_me()).first_name
            return await bot.send_message(
                data["chat"]["id"], f"`Please add {stree} in this group.`"
            )
        except Exception as ex:
            return await bot.send_message(data["chat"]["id"], "`" + str(ex) + "`")
        try:
            full_chat = await bot(GetFullChannelRequest(chat))
        except ValueError:
            stree = (await bot.get_me()).first_name
            return await bot.send_message(
                data["chat"]["id"], f"`Please add {stree} in this group.`"
            )
        except Exception as ex:
            return await bot.send_message(data["chat"]["id"], "`" + str(ex) + "`")
        try:
            call = await bot(GetGroupCallRequest(full_chat.full_chat.call))
        except BaseException:
            call = None
        if not call:
            return await bot.send_message(
                data["chat"]["id"],
                "`I can't access voice chat.`",
            )

        try:
            result = await bot(
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
                data, f"`Joined Voice Chat in {(await bot.get_entity(data['chat']['id'])).title}`",
            )
        except Exception as ex:
            return await bot.send_message(data["chat"]["id"], "`" + str(ex) + "`")

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
