# © 2021 Famhawite Technology & Zoawi Studio without Their permission,
# This Modules is prohibited to re use or modify.

from Sangtei import telethn as tbot
from Sangtei import MONGO_DB_URI
from pymongo import MongoClient
import io
import asyncio
import os
from datetime import datetime

import requests
from telethon import types
from telethon.tl import functions
from Sangtei import REM_BG_API_KEY
from Sangtei import TEMP_DOWNLOAD_DIRECTORY
from Sangtei.events import register


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["Sangtei"]
approved_users = db.approve


@register(pattern="^/rbg")
async def _(event):
    HELP_STR = "he command `/rbg` hi media reply nan hmang rawh"
    if event.fwd_from:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.message.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    if REM_BG_API_KEY is None:
        await event.reply("API key token remove.bg atang in i mamawh he mi hmang ve thei tur chuan.")
        return False
    start = datetime.now()
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        await event.reply("Siam mek...")
        await event.reply("Upload mek...")
        try:
            downloaded_file_name = await tbot.download_media(
                reply_message, TEMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await event.reply(str(e))
            return
        else:
            output_file_name = ReTrieveFile(downloaded_file_name)
            os.remove(downloaded_file_name)
    else:
        await event.reply(HELP_STR)
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "Miss-Sangtei.png"
            await tbot.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id,
            )
    else:
        await event.reply(
            "remove.bg API a dik lo tlat mai. Khawngaih in hetah hian report rawh [Support Group](https://t.me/joinchat/FlMWfMyVSNZjZjhl)\n`{}".format(
                output_file_name.content.decode("UTF-8")
            )
        )


def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    return r
@register(pattern="^/superfban")
async def _(event):
    if event.reply_to_msg_id:
        k = await event.reply("SuperFedban tih tan mek ani..")
        await asyncio.sleep(2)
        await k.edit("User hi feds 222 ah Hlawhtling taka Banned ani")
    else:
        await event.reply("Chin tawk hriat ve a tha e")
        return
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__mod_name__ = "Remove backgrd"

__help__ = """
 - /rbg: Media file kha hemu command hmang hian reply la background chu a rawn remove mai ang
"""
