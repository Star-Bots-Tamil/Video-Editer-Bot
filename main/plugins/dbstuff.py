# (c) Star Bots Tamil

from telethon import events, Button
from decouple import config

from .. import Star_Bots_Tamil, AUTH_USERS, MONGODB_URI

from main.Database.database import Database

#Database Command handling--------------------------------------------------------------------------

db = Database(MONGODB_URI, 'Video-Editer-Bot')

@Star_Bots_Tamil.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def incomming(event):
    if not await db.is_user_exist(event.sender_id):
        await db.add_user(event.sender_id)

@Star_Bots_Tamil.on(events.NewMessage(incoming=True, from_users=AUTH_USERS , pattern="/stats"))
async def listusers(event):
    xx = await event.reply("**Counting Total Users 📊 in Database.**")
    x = await db.total_users_count()
    await xx.edit(f"**Total Users 📊 :- {int(x)}**")

@Star_Bots_Tamil.on(events.NewMessage(incoming=True, from_users=AUTH_USERS , pattern="/broadcast"))
async def bcast(event):
    ids = []
    msg = await event.get_reply_message()
    if not msg:
        await event.reply("**Reply to a Message to Broadcast!**")
    xx = await event.reply("**Counting Total Users 📊 in Database.**")
    x = await db.total_users_count()
    await xx.edit(f"**Total Users 📊 :- {int(x)}**")
    all_users = await db.get_users()
    sent = []
    failed = []
    async for user in all_users:
        user_id = user.get("id", None) 
        ids.append(user_id)
    for id in ids:
        try:
            try:
                await event.client.send_message(int(id), msg)
                sent.append(id)
                await xx.edit(f"**Total Users 📊 :- {x}**", 
                             buttons=[
                                 [Button.inline(f"Sent :- {len(sent)}", data="none")],
                                 [Button.inline(f"Failed :- {len(failed)}", data="none")]])
                await asyncio.sleep(1)
            except FloodWaitError as fw:
                await asyncio.sleep(fw.seconds + 10)
                await event.client.send_message(int(id), msg)
                sent.append(id)
                await xx.edit(f"**Total Users 📊 :- {x}**", 
                             buttons=[
                                [Button.inline(f"Sent :- {len(sent)}", data="none")],
                                [Button.inline(f"Failed :- {len(failed)}", data="none")]])
                await asyncio.sleep(1)
        except Exception:
            failed.append(id)
            await xx.edit(f"**Total Users 📊 :- {x}**", 
                             buttons=[
                                 [Button.inline(f"Sent :- {len(sent)}", data="none")],
                                 [Button.inline(f"Failed :- {len(failed)}", data="none")]])
    await xx.edit(f"**Broadcast 💌 Completed 💯.\n\nTotal Users in Database :- {x}**", 
                 buttons=[
                     [Button.inline(f"Sent :- {len(sent)}", data="none")],
                     [Button.inline(f"Failed :- {len(failed)}", data="none")]])
    
    
@Star_Bots_Tamil.on(events.NewMessage(incoming=True, from_users=AUTH_USERS , pattern="^/disallow (.*)" ))
async def bban(event):
    c = event.pattern_match.group(1)
    if not c:
        await event.reply("**Disallow Who!?**")
    AUTH = config("AUTH_USERS", default=None)
    admins = []
    admins.append(f'{int(AUTH)}')
    if c in admins:
        return await event.reply("**I Can't Ban an AUTH_USER**")
    xx = await db.is_banned(int(c))
    if xx is True:
        return await event.reply("**User is Already Disallowed!**")
    else:
        await db.banning(int(c))
        await event.reply(f"**{c} is Now Disallowed.**")
    admins.remove(f'**{int(AUTH)}**')
    
@Star_Bots_Tamil.on(events.NewMessage(incoming=True, from_users=AUTH_USERS , pattern="^/allow (.*)" ))
async def unbban(event):
    xx = event.pattern_match.group(1)
    if not xx:
        await event.reply("**Allow who?**")
    xy = await db.is_banned(int(xx))
    if xy is False:
        return await event.reply("**User is Already Allowed!**")
    await db.unbanning(int(xx))
    await event.reply(f"**{xx} Allowed!**")
    

    


   
    
