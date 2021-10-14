import os
import subprocess
import sys
from time import sleep

from telegram import TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, run_async

from Sangtei import dispatcher
from Sangtei.modules.helper_funcs.chat_status import dev_plus


@run_async
@dev_plus
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
            update.effective_message.reply_text("Beep boop, He group hi ka chhuahsan e!.")
        except TelegramError:
            update.effective_message.reply_text(
                "Beep boop, he group hi ka chhuahsan thei lo(a chhan pawh ka hre lo)."
            )
    else:
        update.effective_message.reply_text("Send a valid chat ID")


@run_async
@dev_plus
def gitpull(update: Update, context: CallbackContext):
    sent_msg = update.effective_message.reply_text(
        "Thlak danglam na chu a bul thut atangin neih ani, chuan tih nun leh tuma beih mek ani."
    )
    subprocess.Popen("git pull", stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\nThlak danglam mek ani...Ka ngaihdan in.. Tih nun leh mek ani ang "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("Restarted.")

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


@run_async
@dev_plus
def restart(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "Hmanhmawh tak in thil thar chu dah ani a, chuan a hlui zawk hi tih thih ani ang"
    )

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


LEAVE_HANDLER = CommandHandler("leave", leave)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull)
RESTART_HANDLER = CommandHandler("reboot", restart)

dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)

__mod_name__ = "Dev"
__handlers__ = [LEAVE_HANDLER, GITPULL_HANDLER, RESTART_HANDLER]
