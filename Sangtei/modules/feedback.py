import html
from telegram import Update, Bot, ParseMode
from telegram.ext import run_async
from Sangtei.modules.disable import DisableAbleCommandHandler
from Sangtei import dispatcher
from requests import get
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton



@run_async
def feedback(bot: Bot, update: Update):
  name = update.effective_message.from_user.first_name
  message = update.effective_message
  userid=message.from_user.id
  text = message.text[len('/feedback '):]
   

  feed_text = f"Sangtei feedback *Thar* a dawng e, he user [{name}](tg://user?id={userid}) hen atang hian.\n\nfeed: {text}"
  

  bot.send_message(-1001308467547, feed_text, parse_mode=ParseMode.MARKDOWN)
 
  text = html.escape(text)
  reply_text=f"Feedback min pek avang in kan lawm e."
  message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="I feedback chu hetah hian i hmu thei ang",url="https://t.me/Sangtei_Update")]]))
                                               
  

  



help = """
 - /feedback : I feedback hemi command kaltlang hian min thawn thei ang, 
               I feedback pawh i hmu thei bawk ang.
"""

mod_name = "Feedback"

feed_handle = DisableAbleCommandHandler("feedback", feedback)

dispatcher.add_handler(feed_handle)
