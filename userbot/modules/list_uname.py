from telethon import events, functions, types
from userbot.utils.tools import is_admin
from userbot import CMD_HELP, bot
from userbot.events import register
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest

@register(outgoing=True, pattern=r"^.xlist")
async def mine(event):
    """ For .reserved command, get a list of your reserved usernames. """
    result = await bot(GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"{channel_obj.title}\n@{channel_obj.username}\n\n"
    await event.edit(output_str)



CMD_HELP.update(
    {
        "ListUsernames": "**Plugin : **`listusername`\
    \n\n**Syntax : **`.xlist`\
    \n**Function : **this plugin give you your all channel and groups usernamen"
    }
)
