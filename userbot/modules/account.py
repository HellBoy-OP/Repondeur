from telethon import *
from userbot import *
from userbot.utils import *
from userbot.events import *

@register(outgoing=True, pattern=r"^\.deletemyaccount")
async def _(event):
  if event.fwd_from:
        return
  chat = event.chat_id
  async with client.conversation(chat) as conv:
    msg1 = await conv.send_message('Do You Really Want To Delete You Account')
    msg2 = await conv.get_response()
    msg3 = await conv.get_reply()
    x = msg2 or msg3
    y = x.lower()
    if y == "yes":
      await event.edit("I am deleting my account with own faith no one is responsible except me")
      await bot(functions.account.DeleteAccountRequest("I am Deleteing my Account on my own risk"))
    else:
      return await event.edit(f"Since You Havnt Replied me `yes` delete your account I am aborting")

CMD_HELP.update(
    {
        "Delete Account": ">`.deletemyaccount"
        "\nUsage: This Will Delete your account so beware"
    }
)    
