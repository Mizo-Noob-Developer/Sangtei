from Sangtei import dispatcher

from Sangtei.modules.disable import DisableAbleCommandHandler

from telegram import Update

from telegram.ext import CallbackContext, run_async

@run_async def vip(update: Update, context: CallbackContext):
    update.effective_message.reply_text("♡ A hnuai ami te hi kan bot a nun zel theih nan a, sum leh pai hmanga min tanpui tu te, kan tana mi hlu em em te an ni. ♡\n\n● John Dominic (10583181423)")


VIP_HANDLER = DisableAbleCommandHandler("vip", vip)  

dispatcher.add_handler(VIP_HANDLER)  

__command_list__ = [
  "vip",
  ]

__handlers__ = [ 
  VIP_HANDLER,
  ]
