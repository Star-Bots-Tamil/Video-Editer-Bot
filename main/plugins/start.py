# (c) Star Bots Tamil

from telethon import events, Button
from ethon.teleutils import mention
from ethon.mystarts import vc_menu

from .. import Star_Bots_Tamil, ACCESS_CHANNEL, AUTH_USERS

from main.plugins.actions import set_thumbnail, rem_thumbnail, heroku_restart
from Star-Bots-Tamil.localisation import START_TEXT as st
from Star-Bots-Tamil.localisation import spam_notice, help_text, SUPPORT_LINK, source_text, DEV

@Star_Bots_Tamil.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply(f'{st}', 
                      buttons=[
                              [Button.inline("Menu.", data="menu")]
                              ])
    tag = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await Star_Bots_Tamil.send_message(int(ACCESS_CHANNEL), f'{tag} started the BOT')
    
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
                         Button.url("SOURCE", url="https://github.com/nimmni/VIDEOconvertor-personal/"),
                         Button.inline("BACK", data="menu")]])
                                 
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="help"))
async def help(event):
    await event.edit('**👥HELP & SETTINGS**',
                    buttons=[[
                         Button.inline("SET THUMB", data="sett"),
                         Button.inline("REM. THUMB", data='remt')],
                         [
                         Button.inline("ACTIONS", data="actions"),
                         Button.inline("RESTART", data="restart")],
                         [Button.url("SUPPORT", url=f"{SUPPORT_LINK}")],
                         [
                         Button.inline("BACK", data="menu")]])
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="actions"))
async def plugins(event):
    await event.edit(f'{help_text}',
                    buttons=[[Button.inline("Menu.", data="menu")]])
                   
 #-----------------------------------------------------------------------------------------------                            
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="sett"))
async def sett(event):    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Star_Bots_Tamil.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Send me any image for thumbnail as a `reply` to this message.")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("No media found.")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("No image found.")
        await set_thumbnail(event, x.media)
        await xx.delete()
        
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="remt"))
async def remt(event):  
    await event.delete()
    await rem_thumbnail(event)
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="restart"))
async def res(event):
    if not f'{event.sender_id}' == f'{int(AUTH_USERS)}':
        return await event.edit("Only authorized user can restart!")
    result = await heroku_restart()
    if result is None:
        await event.edit("You have not filled `HEROKU_API` and `HEROKU_APP_NAME` vars.")
    elif result is False:
        await event.edit("An error occured!")
    elif result is True:
        await event.edit("Restarting app, wait for a minute.")
