import time

from telethon import events

from Sangtei import telethn
from Sangtei.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages,
    user_is_admin,
)


@telethn.on(events.NewMessage(pattern="^[!/]purge$"))
async def purge_messages(event):
    start = time.perf_counter()
    if event.from_id is None:
        return

    if not await user_is_admin(
        user_id=event.sender_id, message=event
    ) and event.from_id not in [1087968824]:
        await event.reply("He command hi Admin te tan chiah hman phal ani")
        return

    if not await can_delete_messages(message=event):
        await event.reply("He message hi purge theih ani tlat lo")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Khawi atanga purge tur nge hre tur in message reply rawh.")
        return
    messages = []
    message_id = reply_msg.id
    delete_to = event.message.id

    messages.append(event.reply_to_msg_id)
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == 100:
            await event.client.delete_messages(event.chat_id, messages)
            messages = []

    await event.client.delete_messages(event.chat_id, messages)
    time_ = time.perf_counter() - start
    text = f"Purge zawh fel ani e, hun hman rei zawng {time_:0.2f} Second(s)"
    await event.respond(text, parse_mode="markdown")


@telethn.on(events.NewMessage(pattern="^[!/]del$"))
async def delete_messages(event):
    if event.from_id is None:
        return

    if not await user_is_admin(
        user_id=event.sender_id, message=event
    ) and event.from_id not in [1087968824]:
        await event.reply("He command hi Admin te tan chiah hman phal ani")
        return

    if not await can_delete_messages(message=event):
        await event.reply("He message hi paih theih ni in a lang lo?")
        return

    message = await event.get_reply_message()
    if not message:
        await event.reply("Eng nge paih i duh chu?")
        return
    chat = await event.get_input_chat()
    del_message = [message, event.message]
    await event.client.delete_messages(chat, del_message)


__help__ = """
*Admin tan chauh:*
 •  /del : i message reply te paih na
 •  /purge : message zawng zawng paihna leh a inkar ami zawng then fai na.
 •  /purge `<integer X>`: message paih ani e, chuan i message thlan chhuah a reply na awm zawng zawng pawh paih ani.
"""

__mod_name__ = "Purges"
