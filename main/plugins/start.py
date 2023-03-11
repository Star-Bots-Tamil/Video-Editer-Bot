# (c) Star Bots Tamil

from telethon import events, Button
from ethon.mystarts import vc_menu
from .. import Star_Bots_Tamil, ACCESS_CHANNEL, AUTH_USERS

from main.plugins.actions import set_thumbnail, rem_thumbnail, heroku_restart
from StarBotsTamil.presents import START_TEXT as start
from StarBotsTamil.presents import spam_notice, help_text, SUPPORT_LINK, source_text, DEV, about_text, about_text_1

@Star_Bots_Tamil.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    mention = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await event.reply(f"**Hi 👋🏻 {mention} ❤️,\n{start}**", link_preview=False,
                      buttons=[
                              [Button.inline("Bot's Menu", data="menu")],
                              [Button.url("🤖 Bot Channel", url="https://t.me/Star_Bots_Tamil")]
                              ])
    mention = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await Star_Bots_Tamil.send_message(int(ACCESS_CHANNEL), f'{mention} Started The Bot')
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="menu"))
async def menu(event):
    await vc_menu(event)
 
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="notice"))
async def notice(event):
    await event.answer(f'{spam_notice}', alert=True)

@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="source"))
async def source(event):
    await event.edit(source_text,
                    buttons=[[
                         Button.url("Source Code", url="https://bit.ly/3F0pGqK"),
                         Button.inline("Back", data="menu")]])
                                 
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="help"))
async def help(event):
    await event.edit('**👥 Help & ⚙️ Settings**',
                    buttons=[[
                         Button.inline("Set Thumbnail 🏞", data="sett"),
                         Button.inline("Remove Thumbnail 🚫", data='remt')],
                         [
                         Button.inline("🤖 Bot Features", data="actions"),
                         Button.inline("🔄 Restart Bot", data="restart")],
                         [Button.url("👥 Support", url=f"{SUPPORT_LINK}")],
                         [
                         Button.inline("Back", data="menu")]])
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="actions"))
async def plugins(event):
    mention = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await event.edit(f'**Hi 👋🏻 {mention} ❤️,\n\n**{help_text}',
                    buttons=[[Button.inline("Bot's Menu", data="menu")]])
                   
 #-----------------------------------------------------------------------------------------------                            
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="sett"))
async def sett(event):    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Star_Bots_Tamil.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("**Send me any Image for Thumbnail 🏞 as a Reply to This Message.**")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("**No Media Found 🚫.**")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("**No Image Found 🚫.**")
        await set_thumbnail(event, x.media)
        await xx.delete()
        
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="remt"))
async def remt(event):  
    await event.delete()
    await rem_thumbnail(event)
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="restart"))
async def res(event):
    if not f'{event.sender_id}' == f'{int(AUTH_USERS)}':
        return await event.edit("**Only Authorized User Can 🔄 Restart The Bot!**")
    result = await heroku_restart()
    if result is None:
        await event.edit("**You Have Not Full Filled `HEROKU_API` And `HEROKU_APP_NAME` Config Vars.**")
    elif result is False:
        await event.edit("**An Error Occured!**")
    elif result is True:
        await event.edit("**🔄 Restarting Bot 🤖, Wait for a Minute.**")

# Help Command 

@Star_Bots_Tamil.on(events.NewMessage(incoming=True, pattern="/help"))
async def help(event):
    mention = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await event.reply(f'**Hi 👋🏻 {mention} ❤️,\n\n**{help_text}', 
                      buttons=[
                              [Button.url("🤖 Bot Channel", url="https://t.me/Star_Bots_Tamil")]
                              ])

# About Command

@Star_Bots_Tamil.on(events.NewMessage(incoming=True, pattern="/about"))
async def about(event):
    mention = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await event.reply(f'{about_text}\n\n👬🏻 My Best Friend :- {mention} ❤️\n\n{about_text_1}', link_preview=False, 
                      buttons=[
                              [Button.url("🤖 Bot Channel", url="https://t.me/Star_Bots_Tamil")]
                              ])

