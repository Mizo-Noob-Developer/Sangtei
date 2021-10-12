#    Copyright (C) 2020-2021 by @InukaAsith
#    This programme is a part of Liza TG bot project
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging
import time

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from Sangtei import DRAGONS as SUDO_USERS
from Sangtei import pbot
from Sangtei.modules.sql import forceSubscribe_sql as sql

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)


@pbot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
    user_id = cb.from_user.id
    chat_id = cb.message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        channel = chat_db.channel
        chat_member = client.get_chat_member(chat_id, user_id)
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == (client.get_me()).id:
                try:
                    client.get_chat_member(channel, user_id)
                    client.unban_chat_member(chat_id, user_id)
                    cb.message.delete()
                    # if cb.message.reply_to_message.from_user.id == user_id:
                    # cb.message.delete()
                except UserNotParticipant:
                    client.answer_callback_query(
                        cb.id,
                        text=f"❗ Kan channel @{channel} hi join la chuan 'UnMute Me' button hi hmet leh rawh.",
                        show_alert=True,
                    )
            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ Chhan eng emaw avang in admin lam atanga mute i ni.",
                    show_alert=True,
                )
        else:
            if (
                not client.get_chat_member(chat_id, (client.get_me()).id).status
                == "administrator"
            ):
                client.send_message(
                    chat_id,
                    f"❗ **{cb.from_user.mention} hian amah leh amah in UnMuted a tum a, mahse ka UnMuted thei lo, admin ah min dah phawt a ngai.**\n__#Leaving this chat...__",
                )

            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ Warning! Button hi hmet suh group ah i tawng ve theih tawh chuan.",
                    show_alert=True,
                )


@pbot.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
    chat_id = message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        user_id = message.from_user.id
        if (
            not client.get_chat_member(chat_id, user_id).status
            in ("administrator", "creator")
            and not user_id in SUDO_USERS
        ):
            channel = chat_db.channel
            try:
                client.get_chat_member(channel, user_id)
            except UserNotParticipant:
                try:
                    sent_message = message.reply_text(
                        "Chibai {} 🙏 \n **kan channel @{} hi ila join lo a** 🤔 \n \nKhawngaih in [Kan Channel](https://t.me/{}) hi join la ti chuan **UNMUTE ME** Button hi hmet rawh. \n \n ".format(
                            message.from_user.mention, channel, channel
                        ),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Join Channel",
                                        url="https://t.me/{}".format(channel),
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "Min UnMute rawh", callback_data="onUnMuteRequest"
                                    )
                                ],
                            ]
                        ),
                    )
                    client.restrict_chat_member(
                        chat_id, user_id, ChatPermissions(can_send_messages=False)
                    )
                except ChatAdminRequired:
                    sent_message.edit(
                        "❗ **Sangtei hi he tah hian admin ani lo..**\n__Ban permission min pe rawh.. \n#Ending FSub...__"
                    )

            except ChatAdminRequired:
                client.send_message(
                    chat_id,
                    text=f"❗ **He channel @{channel} ah hian admin ka ni lo.**\n__Admin ah min dah la ti nawn leh rawh.\n#Ending FSub...__",
                )


@pbot.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status is "creator" or user.user.id in SUDO_USERS:
        chat_id = message.chat.id
        if len(message.command) > 1:
            input_str = message.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                message.reply_text("❌ **Force Subscribe chu hlawhtling tak a tih thih ani.**")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "**Unmuting all members who are muted by me...**"
                )
                try:
                    for chat_member in client.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == (client.get_me()).id:
                            client.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit("✅ **Member ka mute zawng zawng te UnMuted an ni.**")
                except ChatAdminRequired:
                    sent_message.edit(
                        "❗ **He chat ah hian admin ka ni lo**\n__Member te ka mute thei lo, he group a member te mute thei tur chuan admin ah min dah la member te ban theih na permission nen min pe tel la.__"
                    )
            else:
                try:
                    client.get_chat_member(input_str, "me")
                    sql.add_channel(chat_id, input_str)
                    message.reply_text(
                        f"✅ **Force Subscribe chu tih nun ani**\n__Force Subscribe chu tih nun ani, member zawng zawng ten he [channel](https://t.me/{input_str}) an subscribe vek a ngai, he Group a message te thawn thei tur chuan.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    message.reply_text(
                        f"❗ **Channel ah hian admin ka ni lo**\n__He [channel](https://t.me/{input_str}) hian admin ka ni lo a. ForceSubscribe ti nung tur chuan admin ah min dah rawh.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    message.reply_text(f"❗ **Channel Username a dik lo.**")
                except Exception as err:
                    message.reply_text(f"❗ **ERROR:** ```{err}```")
        else:
            if sql.fs_settings(chat_id):
                message.reply_text(
                    f"✅ **Force Subscribe chu hemi chat bik tan hian tih nun ani.**\n__he [Channel](https://t.me/{sql.fs_settings(chat_id).channel})__ tan hian",
                    disable_web_page_preview=True,
                )
            else:
                message.reply_text("❌ **Force Subscribe chu hemi group bik atan hian tih thih ani.**")
    else:
        message.reply_text(
            "❗ **Group Siamtu i nih angai**\n__He thil ti thei tur hi chuan group siamtu i nih angai.__"
        )


__help__ = """
*ForceSubscribe:*

✪ Sangtei hian member te i channel la subscribe lo tu te a mute thei a
✪ I tih nun hun ah, member la subscribe lo te chu ka mute ang a, UNMUTE button ka pe tel bawk ang tichuan an hmeh hun ah, ka mute na ka ti tawp ang

*Setup*
1) A hmasa ber in i group ah ban permission nei in admin ah min siam la, chuan i channel ah pawh admin ah min dah bawk la.
Note: Group siamtu chauh in min siamrem thei a, siamrem ka nih loh chuan tumah channel subscribe tur in ka nawr lui tawh lo ang.
 
*Commmands*
✪ /ForceSubscribe - Setting awm tawh sa te en na.
✪ /ForceSubscribe no/off/disable - ForceSubscribe tih nun emaw tih thih na.
✪ /ForceSubscribe {channel username} - Tih nun na leh channel siamrem na.
✪ /ForceSubscribe clear - Member ka mute zawng zawng te UNMUTE na.

Note: /FSub hi hemi /ForceSubscribe nen hian a in ang reng

 
"""
__mod_name__ = "Force Subscribe"
