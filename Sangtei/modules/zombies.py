from asyncio import sleep

from telethon import events
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChatBannedRights

from Sangtei import DEV_USERS, DRAGONS, OWNER_ID, TIGERS, telethn

# =================== CONSTANT ===================

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

OFFICERS = [OWNER_ID] + DEV_USERS + DRAGONS + TIGERS

# Check if user has admin rights
async def is_administrator(user_id: int, message):
    admin = False
    async for user in telethn.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in OFFICERS:
            admin = True
            break
    return admin


@telethn.on(events.NewMessage(pattern=f"^[!/]zombies ?(.*)"))
async def zombies(event):
    """ For .zombies command, list all the zombies in a chat. """

    con = event.pattern_match.group(1).lower()
    del_u = 0
    del_status = "Account delete ho hmuh ani lo, Group hi a fai e 🌷"

    if con != "clean":
        find_zombies = await event.respond("Zombie te zawn mek ani...")
        async for user in event.client.iter_participants(event.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f" Zombie **{del_u}** Group ah hian hmuh ani.\
            \nThian fai rawh ti hian :-\n 👉 `/zombies clean`"
        await find_zombies.edit(del_status)
        return

    # Here laying the sanity check
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well

    if not await is_administrator(user_id=event.from_id, message=event):
        await event.respond("Admin pawh i ni bawk lo!")
        return

    if not admin and not creator:
        await event.respond("He tah hian admin ka ni lo!")
        return

    cleaning_zombies = await event.respond("Zombie te then fai mek ani...")
    del_u = 0
    del_a = 0

    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                await cleaning_zombies.edit("He Group ah hian Banned theih na ka nei lo.")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"Zombie `{del_u}` Then fai ani"

    if del_a > 0:
        del_status = f"Zombie `{del_u}` Then fai a ni \
        \n`{del_a}` Zombie Admin Accounts hi then fai ani ve lo!"

    await cleaning_zombies.edit(del_status)


__help__ = """
 ➥ `/zombies`*:* Group ah account delete tawh te an awm em en na leh a chhan na hriat na"""

__mod_name__ = "Zombies"
