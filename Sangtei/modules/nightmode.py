#     (A Telegram Bot Project)
#    Copyright (C) 2019-Present Anonymous (https://t.me/MissJulia_Robot)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, in version 3 of the License.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see < https://www.gnu.org/licenses/agpl-3.0.en.html >


from datetime import timedelta

import dateparser
from telethon import *
from telethon.tl.types import ChatBannedRights

from Sangtei.events import register
from Sangtei.mongo import db
from Sangtei import telethn as tbot

nightmod = db.nightmode


closechat = ChatBannedRights(
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

openchat = ChatBannedRights(
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


def get_info(id):
    return nightmod.find_one({"id": id})


@register(pattern="^/nightmode(?: |$)(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if not await can_change_info(message=event):
        return
    input = event.pattern_match.group(1)
    chats = nightmod.find({})
    if not input:
        for c in chats:
            if event.chat_id == c["id"]:
                await event.reply(
                    "Yes emaw No tih emaw ziak tel rawh.\n\nTuna siam tawh sa chu : **on**"
                )
                return
        await event.reply(
            "Yes emaw No emaw ziak tel rawh.\n\nTuna siam tawh sa chu : **off**"
        )
        return
    if input == "on":
        if event.is_group:
            chats = nightmod.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply("He chat ah hian Nightmode tih nun a ni tawh.")
                    return
            nightmod.insert_one(
                {
                    "id": event.chat_id,
                    "valid": False,
                    "zone": None,
                    "ctime": None,
                    "otime": None,
                }
            )
            await event.reply(
                "He chat ah hian Nightmode tih nun ani.\n**Note:** Hun leh Zone i tih dik loh a hemi `/setnightmode` nen a i siam dik loh chuan hna a thawk thei lo ang"
            )
    if input == "off":
        if event.is_group:
            chats = nightmod.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    nightmod.delete_one({"id": event.chat_id})
                    await event.reply("Nightmode chu he chat ah hian tih thih ani.")
                    return
        await event.reply("Nightmode chu he chat atan hian tih nun ala ni lo.")
    if not input == "on" and not input == "off":
        await event.reply("On emaw Off ti a ziah chiah kha ka hrethiam")
        return


@register(pattern="^/setnightmode (.*)")
async def _(event):
    try:
        if event.fwd_from:
            return
        if event.is_private:
            return
        if not await can_change_info(message=event):
            return
        quew = event.pattern_match.group(1)
        if "|" in quew:
            zone, ctime, otime = quew.split(":")
        zone = zone.strip()
        ctime = ctime.strip()
        otime = otime.strip()
        if len(ctime) != 11:
            await event.reply("Hun leh ni dik tak ziak rawh.")
            return
        if len(otime) != 11:
            await event.reply("Hun leh ni dik tak ziak rawh.")
            return
        if not zone and ctime and otime:
            await event.reply("Anih dan tur dik tak a la ni lo.")
            return
        ttime = dateparser.parse(
            "now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
        )
        if ttime == None or otime == None or ctime == None:
            await event.reply("Hun leh ni leh Zone dik tak ziak rawh.")
            return
        cctime = dateparser.parse(
            f"{ctime}", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "DMY"}
        ) + timedelta(days=1)
        ootime = dateparser.parse(
            f"{otime}", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "DMY"}
        ) + timedelta(days=1)
        if cctime == ootime:
            await event.reply("Chat hawn hun leh khar hun a in ang thei lo.")
            return
        if not ootime > cctime and not cctime < ootime:
            await event.reply("Chat hawn hun hi a khar hun aia hma zawk tur ani")
            return
        if cctime > ootime:
            await event.reply("Chat khar hun hi a hawn hun ai in a hma thei lo")
            return
        # print (ttime)
        # print (cctime)
        # print (ootime)
        chats = nightmod.find({})
        for c in chats:
            if event.chat_id == c["id"] and c["valid"] == True:
                to_check = get_info(
                    id=event.chat_id,
                )
                nightmod.update_one(
                    {
                        "_id": to_check["_id"],
                        "id": to_check["id"],
                        "valid": to_check["valid"],
                        "zone": to_check["zone"],
                        "ctime": to_check["ctime"],
                        "otime": to_check["otime"],
                    },
                    {"$set": {"zone": zone, "ctime": cctime, "otime": ootime}},
                )
                await event.reply(
                    "Nightmode siam fel tawh sa ani.\nZone ka update ang, Khar hun leh hawn hun zone dik tak ah, hawn hun leh khar hun a thawk ang."
                )
                return
        nightmod.insert_one(
            {
                "id": event.chat_id,
                "valid": True,
                "zone": zone,
                "ctime": cctime,
                "otime": ootime,
            }
        )
        await event.reply("Nightmode hlawhtling taka siam ani e !")
    except Exception as e:
        print(e)


@tbot.on(events.NewMessage(pattern=None))
async def _(event):
    try:
        if event.is_private:
            return
        chats = nightmod.find({})
        for c in chats:
            # print(c)
            id = c["id"]
            valid = c["valid"]
            zone = c["zone"]
            ctime = c["ctime"]
            c["otime"]
            present = dateparser.parse(
                f"now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
            )
            if present > ctime and valid:
                await tbot.send_message(
                    id,
                    f"**Zan vengtu:** Tun atan chuan chat theih hun chhung khar a hun ta ...",
                )
                await tbot(
                    functions.messages.EditChatDefaultBannedRightsRequest(
                        peer=id, banned_rights=closechat
                    )
                )
                newtime = ctime + timedelta(days=1)
                to_check = get_info(id=id)
                if not to_check:
                    return
                print(newtime)
                print(to_check)
                nightmod.update_one(
                    {
                        "_id": to_check["_id"],
                        "id": to_check["id"],
                        "valid": to_check["valid"],
                        "zone": to_check["zone"],
                        "ctime": to_check["ctime"],
                        "otime": to_check["otime"],
                    },
                    {"$set": {"ctime": newtime}},
                )
                break
                return
            continue
    except Exception as e:
        print(e)


@tbot.on(events.NewMessage(pattern=None))
async def _(event):
    try:
        if event.is_private:
            return
        chats = nightmod.find({})
        for c in chats:
            # print(c)
            id = c["id"]
            valid = c["valid"]
            zone = c["zone"]
            c["ctime"]
            otime = c["otime"]
            present = dateparser.parse(
                f"now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
            )
            if present > otime and valid:
                await tbot.send_message(
                    id,
                    f"**Zan vengtu:** Chat theih tur a hawn a hun leh ta ...",
                )
                await tbot(
                    functions.messages.EditChatDefaultBannedRightsRequest(
                        peer=id, banned_rights=openchat
                    )
                )
                newtime = otime + timedelta(days=1)
                to_check = get_info(id=id)
                if not to_check:
                    return
                print(newtime)
                print(to_check)
                nightmod.update_one(
                    {
                        "_id": to_check["_id"],
                        "id": to_check["id"],
                        "valid": to_check["valid"],
                        "zone": to_check["zone"],
                        "ctime": to_check["ctime"],
                        "otime": to_check["otime"],
                    },
                    {"$set": {"otime": newtime}},
                )
                break
                return
            continue
    except Exception as e:
        print(e)

__help__ = """
• /setnightmode <time zone> i awmna bial hun bithliah siamna.
• /Nightmode <on/off/enable> nighmode on leh off na tur
"""

__mod_name__ = "Nighmode"
