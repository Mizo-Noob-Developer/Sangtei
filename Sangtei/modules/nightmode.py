from Sangtei.modules.sql.night_mode_sql import add_nightmode, rmnightmode, get_all_chat_id, is_nightmode_indb
from telethon.tl.types import ChatBannedRights
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from telethon import functions
from Sangtei.events import register
from Sangtei import telethn, OWNER_ID
import os
from telethon import *
from telethon import Button, custom, events
hehes = ChatBannedRights(
    until_date=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    send_polls=True,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)
openhehe = ChatBannedRights(
    until_date=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    send_polls=False,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await telethn(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True

async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )

@register(pattern="^/(nightmode|Nightmode|NightMode) ?(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    input = event.pattern_match.group(2)
    if not event.sender_id == OWNER_ID:
        if not await is_register_admin(event.input_chat, event.sender_id):
           await event.reply("Admin chiah in he command hi an hmang thei!")
           return
        else:
          if not await can_change_info(message=dmod):
            await event.reply("You are missing the following rights to use this command:CanChangeinfo")
            return
    if not input:
        if is_nightmode_indb(str(event.chat_id)):
                await event.reply(
                    "He Chat ah hian Nightmode tih nun mek ani"
                )
                return
        await event.reply(
            "He Chat ah hian Nightmode tih thih ani"
        )
        return
    if "on" in input:
        if event.is_group:
            if is_nightmode_indb(str(event.chat_id)):
                    await event.reply(
                        "He Chat ah hian Nightmode tih Nun ani"
                    )
                    return
            add_nightmode(str(event.chat_id))
            await event.reply("NightMode tih nun ani hemi chat tan hian.")
    if "off" in input:
        if event.is_group:
            if not is_nightmode_indb(str(event.chat_id)):
                    await event.reply(
                        "NightMode chu he Chat ah hian tih thih ani"
                    )
                    return
        rmnightmode(str(event.chat_id))
        await event.reply("NightMode Disabled!")
    if not "off" in input and not "on" in input:
        await event.reply("Khawngaihin On emaw Off emaw i hman zawk ti chiang rawh!")
        return


async def job_close():
    chats = get_all_chat_id()
    if len(chats) == 0:
        return
    for pro in chats:
        try:
            await telethn.send_message(
              int(pro.chat_id), "Dar 12:00 Am, a lo ri ta bawk a. Naktuk 6:00 Am, hma chu group hi khar rih ani. Night Mode Tih nun ani e ! \n**Powered By ZoAwi Studio**"
            )
            await telethn(
            functions.messages.EditChatDefaultBannedRightsRequest(
                peer=int(pro.chat_id), banned_rights=hehes
            )
            )
        except Exception as e:
            logger.info(f"He Group {chat} - {e} hi khar theih ani lo")

#Run everyday at 12am
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hour=23, minute=59)
scheduler.start()

async def job_open():
    chats = get_all_chat_id()
    if len(chats) == 0:
        return
    for pro in chats:
        try:
            await telethn.send_message(
              int(pro.chat_id), "06:00 Am, alo ni leh tawh bawk a, Group chu hawn ani leh ta e.\n**Powered By ZoAwi Studio**"
            )
            await telethn(
            functions.messages.EditChatDefaultBannedRightsRequest(
                peer=int(pro.chat_id), banned_rights=openhehe
            )
        )
        except Exception as e:
            logger.info(f"He Group {pro.chat_id} - {e} hi hawn theih ani lo")

# Run everyday at 06
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_open, trigger="cron", hour=5, minute=58)
scheduler.start()

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /nightmode on/off

**Note:** Night Mode hi zan dar 12:00Am(IST) A rik rual in ama tawk in, a in ti nung ang a, Zinglam Dar 6:00Am(IST) A rik rual in ama tawk bawk in a thi leh ang.
"""
__mod_name__ = "NIGHTMODE"
