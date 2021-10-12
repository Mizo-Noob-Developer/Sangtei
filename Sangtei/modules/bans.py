import html

from telegram import ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html

from Sangtei import (
    DEMONS,
    DEV_USERS,
    DRAGONS,
    LOGGER,
    OWNER_ID,
    TIGERS,
    WOLVES,
    dispatcher,
)
from Sangtei.modules.disable import DisableAbleCommandHandler
from Sangtei.modules.helper_funcs.chat_status import (
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    is_user_ban_protected,
    is_user_in_chat,
    user_admin,
    user_can_ban,
)
from Sangtei.modules.helper_funcs.extraction import extract_user_and_text
from Sangtei.modules.helper_funcs.string_handling import extract_time
from Sangtei.modules.log_channel import gloggable, loggable


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot = context.bot
    args = context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("User i ban duh kha mention tel rawh.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User hi hmuh ani lo":
            message.reply_text("Tuna i zawn mek hi ka hmu thei lo.")
            return log_message
        else:
            raise

    if user_id == bot.id:
        message.reply_text("Mai mai chuan, keimah leh keimah ka in ban ang maw, noob!")
        return log_message

    if is_user_ban_protected(chat, user_id, member) and user not in DEV_USERS:
        if user_id == OWNER_ID:
            message.reply_text("Min siam tu te zing a mi ban tur in min ti leh a maw?")
            return log_message
        elif user_id in DEV_USERS:
            message.reply_text("Keimahni lam te ka hnehchhuh thei lo.")
            return log_message
        elif user_id in DRAGONS:
            message.reply_text(
                "Min siamtu te zing a mi bei tur a min tih hian, he group a member te dinhmun hlauhthawnawm ah i dah aw."
            )
            return log_message
        elif user_id in DEMONS:
            message.reply_text(
                "Min Siamtu Demon Disaster te zing a mi bei thei tur chuan @Sangtei_update atangin phalna la rawh."
            )
            return log_message
        elif user_id in TIGERS:
            message.reply_text(
                "Min siamtu Tiger disaster te zing ami i bei duh anih chuan @Sangtei_update atangin phalna la rawh."
            )
            return log_message
        elif user_id in WOLVES:
            message.reply_text("Wolf ho ang a theihna i neih chuan ban theihna a ti pung ang!")
            return log_message
        else:
            message.reply_text("He user hian theihna sang tak a nei a, banned theih ani lo.")
            return log_message

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#BANNED\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        chat.kick_member(user_id)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        reply = (
            f"<code>❕</code><b>Ban Event</b>\n"
            f"<code> </code><b>•  User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            reply += f"\n<code> </code><b>•  A chhan:</b> \n{html.escape(reason)}"
        bot.sendMessage(chat.id, reply, parse_mode=ParseMode.HTML, quote=False)
        return log

    except BadRequest as excp:
        if excp.message == "I message reply hi hmuh ani lo":
            # Do not reply
            message.reply_text("Banned!", quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "User %s kan chat %s (%s) a awm hi a Banned theih loh a chhan chu %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("Uhm...hna a thawk theilo ni in a lang...")

    return log_message


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def temp_ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("User i ban tur kha mention tel rawh.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User hmuh ani lo":
            message.reply_text("He user hi hmuh ani lo.")
            return log_message
        else:
            raise

    if user_id == bot.id:
        message.reply_text("Keimah leh keimah ka in BAN nguar ang, i â em ni?")
        return log_message

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("Ka ngainat zawng ani ve lo.")
        return log_message

    if not reason:
        message.reply_text("He user hi BAN tur hun chhung i ziak tel lo a!")
        return log_message

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    bantime = extract_time(message, time_val)

    if not bantime:
        return log_message

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        "#TEMP BANNED\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
        f"<b>Time:</b> {time_val}"
    )
    if reason:
        log += "\n<b>A chhan:</b> {}".format(reason)

    try:
        chat.kick_member(user_id, until_date=bantime)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"Banned! User {mention_html(member.user.id, html.escape(member.user.first_name))} "
            f"will be banned for {time_val}.",
            parse_mode=ParseMode.HTML,
        )
        return log

    except BadRequest as excp:
        if excp.message == "I message reply hi hmuh ani lo":
            # Do not reply
            message.reply_text(
                f"Ban ani! User hi hemi hun chhung {time_val} atan hian ban ani.", quote=False
            )
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "Use %s hi he chat %s (%s) ah hian a ban theih loh, a chhan chu %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("Hrep chuan, He user hi ka ban thei lo.")

    return log_message


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def kick(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("User i kick duh kha mention tel rawh.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User hmuh ani lo":
            message.reply_text("He user hi ka hmu thei lo tlat mai.")
            return log_message
        else:
            raise

    if user_id == bot.id:
        message.reply_text("Aww, he thil hi ka ti miah lo ang.")
        return log_message

    if is_user_ban_protected(chat, user_id):
        message.reply_text("He user hi ka chum chawrh theih ka beisei....")
        return log_message

    res = chat.unban_member(user_id)  # unban on current user = kick
    if res:
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"One Punched! {mention_html(member.user.id, html.escape(member.user.first_name))}.",
            parse_mode=ParseMode.HTML,
        )
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#KICKED\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            log += f"\n<b>A chhan:</b> {reason}"

        return log

    else:
        message.reply_text("Hrep chuan, he user hi ka chum chawrh thei lo.")

    return log_message


@run_async
@bot_admin
@can_restrict
def punchme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("Tih theih chu ka duh... mahse nang chu admin i ni si a.")
        return

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text("*group atangin an chum chhuak che*")
    else:
        update.effective_message.reply_text("Huh? Ka thei lo :/")


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def unban(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("User i Unbanned duh kha mention tel rawh.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User hmuh ani lo":
            message.reply_text("He user hi ka hmu thei tlat lo mai.")
            return log_message
        else:
            raise

    if user_id == bot.id:
        message.reply_text("Hetah ka awm loh chuan engtin nge keimah ka in Unbanned theih ang...?")
        return log_message

    if is_user_in_chat(chat, user_id):
        message.reply_text("He mi hi hetah hian a awm tawh sa ani lawm ni??")
        return log_message

    chat.unban_member(user_id)
    message.reply_text("Aww, he user hian a join leh thei e!")

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNBANNED\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += f"\n<b>A chhan:</b> {reason}"

    return log


@run_async
@connection_status
@bot_admin
@can_restrict
@gloggable
def selfunban(context: CallbackContext, update: Update) -> str:
    message = update.effective_message
    user = update.effective_user
    bot, args = context.bot, context.args
    if user.id not in DRAGONS or user.id not in TIGERS:
        return

    try:
        chat_id = int(args[0])
    except:
        message.reply_text("Chat ID dik tak min pe rawh.")
        return

    chat = bot.getChat(chat_id)

    try:
        member = chat.get_member(user.id)
    except BadRequest as excp:
        if excp.message == "User hmuh ani lo":
            message.reply_text("He user hi ka hmu thei tlat lo.")
            return
        else:
            raise

    if is_user_in_chat(chat, user.id):
        message.reply_text("Chat ah hian i awm tawh sa ani lo em ni??")
        return

    chat.unban_member(user.id)
    message.reply_text("Aww, Ka unbanned tawh che.")

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNBANNED\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )

    return log


__help__ = """
 •  /punchme *:* He command hmang tu tawh phawt user chu, group atangin ka chum chhuak zel ang

*Admins only:*
 •  /ban `<userhandle>` *:* bans a user. (via handle, or reply)
 •  /tban `<userhandle> x(m/h/d)` *:* bans a user for `x` time. (via handle, or reply). `m` = `minutes`, `h` = `hours`, `d` = `days`.
 •  /unban `<userhandle>` *:* unbans a user. (via handle, or reply)
 •  /kick `<userhandle>` *:* Punches a user out of the group, (via handle, or reply)
"""

BAN_HANDLER = CommandHandler("ban", ban)
TEMPBAN_HANDLER = CommandHandler(["tban"], temp_ban)
PUNCH_HANDLER = CommandHandler("kick", kick)
UNBAN_HANDLER = CommandHandler("unban", unban)
ROAR_HANDLER = CommandHandler("roar", selfunban)
PUNCHME_HANDLER = DisableAbleCommandHandler("punchme", punchme, filters=Filters.group)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(PUNCH_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
dispatcher.add_handler(ROAR_HANDLER)
dispatcher.add_handler(PUNCHME_HANDLER)

__mod_name__ = "Bans"
__handlers__ = [
    BAN_HANDLER,
    TEMPBAN_HANDLER,
    PUNCH_HANDLER,
    UNBAN_HANDLER,
    ROAR_HANDLER,
    PUNCHME_HANDLER,
]
