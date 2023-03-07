# (c) Star Bots Tamil

import os, time, asyncio
from telethon import events, Button
from telethon.tl.types import DocumentAttributeVideo
from . import fast_download
from ethon.pyfunc import video_metadata

from .. import Star_Bots_Tamil, LOG_CHANNEL, FORCESUB_UN, MONGODB_URI, ACCESS_CHANNEL

from main.plugins.rename import media_rename
from main.plugins.compressor import compress
from main.plugins.trimmer import trim
from main.plugins.convertor import mp3, flac, wav, mp4, mkv, webm, file, video
from main.Database.database import Database
from main.plugins.actions import force_sub
from main.plugins.encoder import encode
from main.plugins.ssgen import screenshot
from StarBotsTamil.presents import source_text, SUPPORT_LINK

#Don't be a MF by stealing someone's hardwork.
forcesubtext = f"**Hey there!To use this bot you've to join @{FORCESUB_UN}.\n\nAlso join @Star_Bots_Tamil.**"

@Star_Bots_Tamil.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def compin(event):
    db = Database(MONGODB_URI, 'Video-Editer-Bot')
    if event.is_private:
        media = event.media
        if media:
            yy = await force_sub(event.sender_id)
            if yy is True:
                return await event.reply(forcesubtext)
            banned = await db.is_banned(event.sender_id)
            if banned is True:
                return await event.reply(f'**You are Banned to Use me!\n\nContact :- [Star Bots Tamil Support]({SUPPORT_LINK})**', link_preview=False)
            video = event.file.mime_type
            if 'video' in video:
                await event.reply("Choose Your Appropriate Action 👇🏻",
                            buttons=[
                                [Button.inline("📊 Encoder", data="encode"),
                                 Button.inline("🗜️ Compressor", data="compress")],
                                [Button.inline("🔄 Converter", data="convert"),
                                 Button.inline("✍🏻 Renamer", data="rename")],
                                [Button.inline("🖼️ Screen Shots", data="sshots"),
                                 Button.inline("✂️ Trimmer", data="trim")]
                            ])
            elif 'png' in video:
                return
            elif 'jpeg' in video:
                return
            elif 'jpg' in video:
                return    
            else:
                await event.reply('**✍🏻Rename Your File 📂**',
                            buttons=[  
                                [Button.inline("✍🏻 Renamer", data="rename")]])
    await event.forward_to(int(ACCESS_CHANNEL))
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="encode"))
async def _encode(event):
    await event.edit("**📊 Encode Your File 📂**",
                    buttons=[
                        [Button.inline("240p", data="240"),
                         Button.inline("360p", data="360")],
                        [Button.inline("480p", data="480"),
                         Button.inline("720p", data="720")],
                        [Button.inline("x264", data="264"),
                         Button.inline("x265", data="265")],
                        [Button.inline("👈🏻 Back", data="back")]])
     
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="compress"))
async def _compress(event):
    await event.edit("**🗜 Compress Your File 📂**",
                    buttons=[
                        [Button.inline("HEVC Compress", data="hcomp"),
                         Button.inline("🏎️ Fast Compress", data="fcomp")],
                        [Button.inline("👈🏻 Back", data="back")]])

@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="convert"))
async def convert(event):
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.edit("**🔄 Convert Your File 📂\n✶ If You Want to Set Custom Thumbnail 🖼️ on Video 🎥 / File 📂, Then First Send an Image 🖼️ and Save as Custom Thumbnail 🖼️.\nChoose Your Appropriate Action 👇🏻**",
                    buttons=[
                        [Button.inline("Convert to mp3", data="mp3"),
                         Button.inline("Convert to flac", data="flac"),
                         Button.inline("Convert to wav", data="wav")],
                        [Button.inline("Convert to mp4", data="mp4"),
                         Button.inline("Convert to webm", data="webm"),
                         Button.inline("Convert to mkv", data="mkv")],
                        [Button.inline("Convert as File 📂", data="file"),
                         Button.inline("Convert as Video 🎥", data="video")],
                        [Button.inline("👈🏻 Back", data="back")]])
                        
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="back"))
async def back(event):
    await event.edit("**Choose Your Appropriate Action 👇🏻** ", buttons=[
                    [Button.inline("📊 Encoder", data="encode"),
                     Button.inline("🗜️ Compressor", data="compress")],
                    [Button.inline("🔄 Converter", data="convert"),
                     Button.inline("✍🏻 Renamer", data="rename")],
                    [Button.inline("🖼️ Screen Shots", data="sshots"),
                     Button.inline("✂️ Trimmer", data="trim")]])
    
#-----------------------------------------------------------------------------------------

process1 = []
timer = []

#Set timer to avoid spam
async def set_timer(event, list1, list2):
    now = time.time()
    list2.append(f'{now}')
    list1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, '**You can Start a New Process Again After 5 Minutes.')
    await asyncio.sleep(300)
    list2.pop(int(timer.index(f'{now}')))
    list1.pop(int(process1.index(f'{event.sender_id}')))
    
#check time left in timer
async def check_timer(event, list1, list2):
    if f'{event.sender_id}' in list1:
        index = list1.index(f'{event.sender_id}')
        last = list2[int(index)]
        present = time.time()
        return False, f"**You Have to Wait {300-round(present-float(last))} Seconds More to Start a New Process!**"
    else:
        return True, None
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="mp3"))
async def vtmp3(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await mp3(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("**Another Process in Progress!**")
        
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="flac"))
async def vtflac(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await flac(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("**Another Process in Progress!**")
        
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="wav"))
async def vtwav(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await wav(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("**Another Process in Progress!**")
        
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="mp4"))
async def vtmp4(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await mp4(event, msg)
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="mkv"))
async def vtmkv(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await mkv(event, msg)  
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="webm"))
async def vtwebm(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await webm(event, msg)  
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="file"))
async def vtfile(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await file(event, msg)    

@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="video"))
async def ftvideo(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await video(event, msg)
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="rename"))
async def rename(event):    
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    markup = event.client.build_reply_markup(Button.force_reply())
    async with Star_Bots_Tamil.conversation(event.chat_id) as conv: 
        cm = await conv.send_message("**Send me a New Name for the File as a Reply to This Message.**\n\n❗Note :- .ext is Not Required.**", buttons=markup)                              
        try:
            m = await conv.get_reply()
            new_name = m.text
            await cm.delete()                    
            if not m:                
                return await cm.edit("**No Response Found.**")
        except Exception as e: 
            print(e)
            return await cm.edit("**An Error Occured While Waiting for the Response.**")
    await media_rename(event, msg, new_name)  
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="fcomp"))
async def fcomp(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"**You Have to Wait {300-round(present-float(last))} Seconds more to Start a New Process!**", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=2)
        os.rmdir("encodemedia")
        now = time.time()
        timer.append(f'{now}')
        process1.append(f'{event.sender_id}')
        await event.client.send_message(event.chat_id, '**You Can Start a New Process Again After 5 Minutes.**')
        await asyncio.sleep(300)
        timer.pop(int(timer.index(f'{now}')))
        process1.pop(int(process1.index(f'{event.sender_id}')))
    else:
        await event.edit(f"**Another Process in Progress!\n\n[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
                       
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="hcomp"))
async def hcomp(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"You have to wait {300-round(present-float(last))} seconds more to start a new process!", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=1)
        os.rmdir("encodemedia")
        now = time.time()
        timer.append(f'{now}')
        process1.append(f'{event.sender_id}')
        await event.client.send_message(event.chat_id, '**You Can Start a New Process Again After 5 Minutes.')
        await asyncio.sleep(300)
        timer.pop(int(timer.index(f'{now}')))
        process1.pop(int(process1.index(f'{event.sender_id}')))
    else:
        await event.edit(f"**Another Process in Progress!\n\n[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)

@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="264"))
async def _264(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=4, ps_name="**ENCODING:**")
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Another Process in Progress!\n\n[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
      
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="265"))
async def _265(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=3, ps_name="**ENCODING:**")
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Another Process in Progress!\n\n[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
        
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="240"))
async def _240(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=240)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Another Process in Progress!\n\n[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
        
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="360"))
async def _360(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=360)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Another Process in Progress!\n\n[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
        
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="480"))
async def _480(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=480)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Another Process in Progress!\n\n[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
        
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="720"))
async def _720(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=720)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Another Process in Progress!\n\n[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
          
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="sshots"))
async def ss_(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"**You Have to Wait {120-round(present-float(last))} Seconds More to Start a New Process!**", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    await screenshot(event, msg)    
    now = time.time()
    timer.append(f'{now}')
    process1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, '**You Can Start a New Process Again After 2 Minutes.**')
    await asyncio.sleep(120)
    timer.pop(int(timer.index(f'{now}')))
    process1.pop(int(process1.index(f'{event.sender_id}')))
    
@Star_Bots_Tamil.on(events.callbackquery.CallbackQuery(data="trim"))
async def vtrim(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    markup = event.client.build_reply_markup(Button.force_reply())
    async with Star_Bots_Tamil.conversation(event.chat_id) as conv: 
        try:
            xx = await conv.send_message("**Send me the Start Time of The Video You Want to Trim From as a Reply to This.\n\nIn Format hh:mm:ss , for Example :- `01:20:69`**", buttons=markup)
            x = await conv.get_reply()
            st = x.text
            await xx.delete()                    
            if not st:               
                return await xx.edit("**No Response Found.**")
        except Exception as e: 
            print(e)
            return await xx.edit("An error occured while waiting for the response.")
        try:
            xy = await conv.send_message("**Send me the End 🔚 Time of The Video you Want to Trim till as a Reply to This. \n\nIn Format hh:mm:ss , for Example :- `01:20:69`**", buttons=markup)
            y = await conv.get_reply()
            et = y.text
            await xy.delete()                    
            if not et:                
                return await xy.edit("**No Response Found.**")
        except Exception as e: 
            print(e)
            return await xy.edit("**An Error Occured While Waiting for the Response.**")
        await trim(event, msg, st, et)
