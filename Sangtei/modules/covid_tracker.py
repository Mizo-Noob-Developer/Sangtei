import json
import requests
from urllib.request import urlopen
from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, MessageFilter, run_async

from Sangtei import dispatcher
from Sangtei.modules.disable import DisableAbleCommandHandler
from requests import get
from telegram.ext import CallbackContext

def covindia(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    state = ''
    confirmed = 0
    deceased = 0
    recovered = 0
    state_input = ''.join([message.text.split(' ')[i] + ' ' for i in range(1, len(message.text.split(' ')))]).strip()
    if state_input:
        url_india = 'https://api.covid19india.org/data.json'
        json_url = urlopen(url_india)
        state_dict = json.loads(json_url.read())
        for sdict in state_dict['statewise']:
            if sdict['state'].lower() == state_input.lower():
                confirmed = sdict['confirmed']
                deceased = sdict['deaths']
                recovered = sdict['recovered']
                state = sdict['state']
                break
    
    if state:
        bot.send_message(
            message.chat.id,
            '`COVID-19 Tracker`\n*%s a covid kai tawh zat* : %s\n*Thih pui:* %s\n*Dam chhuak:* %s\n\n_Source:_ covid19india.org' % (state, confirmed, deceased, recovered),
            parse_mode = ParseMode.MARKDOWN,
            disable_web_page_preview = True
        )
    else:
        bot.send_message(
            message.chat.id,
            'India state khawi emaw ber hmang rawh!',
            parse_mode = ParseMode.MARKDOWN,
            disable_web_page_preview = True
        )
@run_async
def corona(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    device = message.text[len('/corona '):]
    fetch = get(f'https://coronavirus-tracker-api.herokuapp.com/all')

    if fetch.status_code == 200:
        usr = fetch.json()
        data = fetch.text
        parsed = json.loads(data)
        total_confirmed_global = parsed["latest"]["confirmed"]
        total_deaths_global = parsed["latest"]["deaths"]
        total_recovered_global = parsed["latest"]["recovered"]
        active_cases_covid19 = total_confirmed_global - total_deaths_global - total_recovered_global
        reply_text = ("*Corona Stats🦠:*\n"
        "Tih chian tawh: `" + str(total_confirmed_global) + "`\n"
        "Thih pui zat: `" + str(total_deaths_global) + "`\n"
        "Dam chhuak zat: `" + str(total_recovered_global) +"`\n"
        "Vei lai mek: `"+ str(active_cases_covid19) + "`")
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

        return

    elif fetch.status_code == 404:
        reply_text = "API lam a down rih tlat mai."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

__help__ = """
 ➥ /covid: Khawvel pumpui Covid Chungchang en na
 ➥ /covindia <state>: Indian state khawi lai pawh Covid statistics hre tur in state hming nen i zawng thei.
"""

__mod_name__ = 'Covid tracker'

COV_INDIA_HANDLER = CommandHandler('covindia', covindia)
CORONA_HANDLER = DisableAbleCommandHandler("covid", corona, admin_ok=True)
dispatcher.add_handler(CORONA_HANDLER)
dispatcher.add_handler(COV_INDIA_HANDLER)
