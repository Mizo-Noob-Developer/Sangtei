from Sangtei import pbot as app
from Sangtei.utils.dbfunc import get_couple, save_couple
from pyrogram import filters
import random
from datetime import datetime

# Date and time
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(' ')
    return dt_list


def dt_tom():
    a = str(int(dt()[0].split('/')[0]) + 1)+"/" + \
        dt()[0].split('/')[1]+"/" + dt()[0].split('/')[2]
    return a


today = str(dt()[0])
tomorrow = str(dt_tom())


@app.on_message(filters.command("couples") & ~filters.edited)
async def couple(_, message):
    if message.chat.type == "private":
        await message.reply_text("He command hi Group a hman atan chauh ani.")
        return
    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            list_of_users = []
            async for i in app.iter_chat_members(message.chat.id):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)
            if len(list_of_users) < 2:
                await message.reply_text("User an la tam tawk lo")
                return
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            c1_mention = (await app.get_users(c1_id)).mention
            c2_mention = (await app.get_users(c2_id)).mention

            couple_selection_message = f"""**Vawiin atan a kan group Nupa thar te:**
{c1_mention} + {c2_mention} = ❤️
__Kan Group Nupa thar tur te hi  12AM {tomorrow}__ ah thlan leh an ni ang"""
            await app.send_message(
                message.chat.id,
                text=couple_selection_message
            )
            couple = {
                "c1_id": c1_id,
                "c2_id": c2_id
            }
            await save_couple(chat_id, today, couple)

        elif is_selected:
            c1_id = int(is_selected['c1_id'])
            c2_id = int(is_selected['c2_id'])
            c1_name = (await app.get_users(c1_id)).first_name
            c2_name = (await app.get_users(c2_id)).first_name
            couple_selection_message = f"""Vawiin atan a kan group Nupa thar te:
[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = ❤️
__Kan Group Nupa thar tur te hi 12AM {tomorrow}__ ah thlan leh an ni ang"""
            await app.send_message(
                message.chat.id,
                text=couple_selection_message
            )
    except Exception as e:
        print(e)
        await message.reply_text(e)



__help__ = """
 ❍ /couples - To Choose Couple Of The Day
 """
__mod_name__ = "⚡️Couples⚡️"

