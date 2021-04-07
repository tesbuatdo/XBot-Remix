from userbot import bot, API_KEY, API_HASH, STRING_SESSION
from telethon.sync import TelegramClient
from pytgcalls import PyTgCalls

from userbot.callsmusic import queues

jemboed = TelegramClient(STRING_SESSION, API_KEY, API_HASH)
pytgcalls = PyTgCalls(jemboed)



@pytgcalls.on_stream_end()
def on_stream_end(chat_id: int) -> None:
    queues.task_done(chat_id)

    if queues.is_empty(chat_id):
        pytgcalls.leave_group_call(chat_id)
    else:
        pytgcalls.change_stream(
            chat_id, queues.get(chat_id)["file_path"]
        )


run = pytgcalls.run
