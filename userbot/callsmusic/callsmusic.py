from userbot import bot
from pytgcalls import PyTgCalls

from userbot.callsmusic import queues

pytgcalls = PyTgCalls(bot)



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
