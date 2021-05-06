from telegram import Update
from telegram.ext import CallbackContext, run_async

from Lyci import dispatcher
from Lyci.modules.disable import DisableAbleCommandHandler

EHI_STRINGS = "Here, new ehi files by @LyciBot 👸\n\n👉 https://www.mediafire.com/folder/eg7gpj68di622/LyciBot"


@run_async
def ehi(update: Update, context: CallbackContext):
    update.effective_message.reply_text(EHI_STRINGS)


EHI_HANDLER = DisableAbleCommandHandler("ehi", ehi)
dispatcher.add_handler(EHI_HANDLER)
