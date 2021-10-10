import html
from typing import Optional

from telegram import Bot, Chat, ChatPermissions, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html

from Sangtei import LOGGER, TIGERS, dispatcher
from Sangtei.modules.helper_funcs.chat_status import (
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    user_admin,
)
from Sangtei.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from Sangtei.modules.helper_funcs.string_handling import extract_time
from Sangtei.modules.log_channel import loggable


def check_user(user_id: int, bot: Bot, chat: Chat) -> Optional[str]:
    if not user_id:
        reply = "User hming emaw a id emaw dik tak min pe lo tlat.."
        return reply

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User hi hmuh ani lo":
            reply = "He user hi ka hmu thei lo tlat"
            return reply
        else:
            raise

    if user_id == bot.id:
        reply = "Keimah leh keimah ka in Muted nguar ang, I kai viau em ni?"
        return reply

    if is_user_admin(chat, user_id, member) or user_id in TIGERS:
        reply = "A theih loh. Ani tih loh hi chu mute tur ka hmu lo."
        return reply

    return None


@run_async
@connection_status
@bot_admin
@user_admin
@loggable
def mute(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id, reason = extract_user_and_text(message, args)
    reply = check_user(user_id, bot, chat)

    if reply:
        message.reply_text(reply)
        return ""

    member = chat.get_member(user_id)

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#MUTE\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    if reason:
        log += f"\n<b>A chhan:</b> {reason}"

    if member.can_send_messages is None or member.can_send_messages:
        chat_permissions = ChatPermissions(can_send_messages=False)
        bot.restrict_chat_member(chat.id, user_id, chat_permissions)
        bot.sendMessage(
            chat.id,
            f"Muted <b>{html.escape(member.user.first_name)}</b> tâwp chin awm lo in!",
            parse_mode=ParseMode.HTML,
        )
        return log

    else:
        message.reply_text("He user hi muted ani tawh!")

    return ""


@run_async
@connection_status
@bot_admin
@user_admin
@loggable
def unmute(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "Unmute tur un username dik tak min pe rawh, emaw an mahni kha unmuted tur in reply mai rawh."
        )
        return ""

    member = chat.get_member(int(user_id))

    if member.status != "kicked" and member.status != "left":
        if (
            member.can_send_messages
            and member.can_send_media_messages
            and member.can_send_other_messages
            and member.can_add_web_page_previews
        ):
            message.reply_text("He user hian ṭawng tur in dikna anei.")
        else:
            chat_permissions = ChatPermissions(
                can_send_messages=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_send_polls=True,
                can_change_info=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
            )
            try:
                bot.restrict_chat_member(chat.id, int(user_id), chat_permissions)
            except BadRequest:
                pass
            bot.sendMessage(
                chat.id,
                f"He user <b>{html.escape(member.user.first_name)}</b> hi a thuziah remtih sak ani ang!",
                parse_mode=ParseMode.HTML,
            )
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#UNMUTE\n"
                f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
            )
    else:
        message.reply_text(
            "He user hi he chat ah hian a la awm lo, unmute ringawt in eng thil tih theihna mah a pe lo ang ang "
            "ti tawh reng a lawm!"
        )

    return ""


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_mute(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id, reason = extract_user_and_text(message, args)
    reply = check_user(user_id, bot, chat)

    if reply:
        message.reply_text(reply)
        return ""

    member = chat.get_member(user_id)

    if not reason:
        message.reply_text("Engtia rei nge mute tur tih a hun i ti chiang lo tlat!")
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    mutetime = extract_time(message, time_val)

    if not mutetime:
        return ""

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#TEMP MUTED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}\n"
        f"<b>Time:</b> {time_val}"
    )
    if reason:
        log += f"\n<b>A chhan:</b> {reason}"

    try:
        if member.can_send_messages is None or member.can_send_messages:
            chat_permissions = ChatPermissions(can_send_messages=False)
            bot.restrict_chat_member(
                chat.id, user_id, chat_permissions, until_date=mutetime
            )
            bot.sendMessage(
                chat.id,
                f"User <b>{html.escape(member.user.first_name)}</b> hi {time_val} chhung atan muted ani!",
                parse_mode=ParseMode.HTML,
            )
            return log
        else:
            message.reply_text("He user hi mute ani tawh.")

    except BadRequest as excp:
        if excp.message == "Message reply hi hmuh ani lo":
            # Do not reply
            message.reply_text(f"{time_val} chhung atan!", quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "He user %s hi chat ah hian %s mute theih ani rih lo (%s) a chhan chu %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("Mai mai chuan, He user hi ka mute thei lo.")

    return ""


__help__ = """
*Admins tan chauh:*
 •  /mute `<userhandle>` *:* user te ngawih tir hmak na. Reply na ah pawh a hman theih, user i reply kha a mute hmak ang.
 •  /tmute `<userhandle> x(m/h/d)` *:* user te mute chhung rei zawng x hun chhung atan. (An mahni kal tlang emaw, an thuziak reply in). `m` = `minutes`, `h` = `hours`, `d` = `days`.
 •  /unmute `<userhandle>` *:* user unmute na. Reply na atang pawn a hman theih, an mahni i reply khan user kha a unmute ang.
"""

MUTE_HANDLER = CommandHandler("mute", mute)
UNMUTE_HANDLER = CommandHandler("unmute", unmute)
TEMPMUTE_HANDLER = CommandHandler(["tmute", "tempmute"], temp_mute)

dispatcher.add_handler(MUTE_HANDLER)
dispatcher.add_handler(UNMUTE_HANDLER)
dispatcher.add_handler(TEMPMUTE_HANDLER)

__mod_name__ = "Muting 🔇"
__handlers__ = [MUTE_HANDLER, UNMUTE_HANDLER, TEMPMUTE_HANDLER]
