# (c) Star Bots Tamil

import asyncio, time, subprocess, re, os

from datetime import datetime as dt
from telethon import events
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from telethon.tl.types import DocumentAttributeVideo
from fasttelethonhelper import fast_download, fast_upload
from ethon.pyfunc import video_metadata

from .. import Star_Bots_Tamil, BOT_UN, LOG_CHANNEL

from main.plugins.actions import LOG_START, LOG_END
from StarBotsTamil.presents import SUPPORT_LINK, JPG, JPG2, JPG3
from StarBotsTamil.utils import ffmpeg_progress

async def encode(event, msg, scale=0):
    ps_name = str(f"**{scale}p Encoding Your File 📂**")
    _ps = str(f"{scale}p ENCODE")
    Star_Bots_Tamil = event.client
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "Trying to process.", reply_to=msg.id)
    new_name = "out_" + dt.now().isoformat("_", "seconds")
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    mime = msg.file.mime_type
    if 'mp4' in mime:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
        out = new_name + ".mp4"
    elif msg.video:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
        out = new_name + ".mp4"
    elif 'x-matroska' in mime:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
        out = new_name + ".mp4"            
    elif 'webm' in mime:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".webm" 
        out = new_name + ".mp4"
    else:
        n = msg.file.name
        ext = (n.split("."))[1]
        out = new_name + ext
    DT = time.time()
    log = await LOG_START(event, f'**{_ps} Process Started\n\n[Bot is busy now]({SUPPORT_LINK})**')
    log_end_text = f'**{_ps} Process Finished\n\n[Bot is free now]({SUPPORT_LINK})**'
    try:
        await fast_download(n, file, Star_Bots_Tamil, edit, DT, "**Downloading Your File 📂**")
    except Exception as e:
        os.rmdir("encodemedia")
        await log.delete()
        await LOG_END(event, log_end_text)
        print(e)
        return await edit.edit(f"**An Error Occured While Downloading.\n\nContact :- [Star Bots Tamil Support]({SUPPORT_LINK})**", link_preview=False) 
    name = '__' + dt.now().isoformat("_", "seconds") + ".mp4"
    os.rename(n, name)
    await edit.edit("Extracting metadata...")
    vid = video_metadata(name)
    hgt = int(vid['height'])
    wdt = int(vid['width'])
    if scale == hgt:
        os.rmdir("encodemedia")
        return await edit.edit(f"The video is already in {scale}p resolution.")
    if scale == 240:
        if 426 == wdt:
            os.rmdir("encodemedia")
            return await edit.edit(f"The video is already in {scale}p resolution.")
    if scale == 360:
        if 640 == wdt:
            os.rmdir("encodemedia")
            return await edit.edit(f"The video is already in {scale}p resolution.")
    if scale == 480:
        if 854 == wdt:
            os.rmdir("encodemedia")
            return await edit.edit(f"The video is already in {scale}p resolution.")
    if scale == 720:
        if 1280 == wdt:
            os.rmdir("encodemedia")
            return await edit.edit(f"The video is already in {scale}p resolution.")
    FT = time.time()
    progress = f"progress-{FT}.txt"
    cmd = ''
    if scale == 240:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -c:v libx264 -pix_fmt yuv420p -preset faster -s 426x240 -crf 24 -c:a libopus -ac 2 -ab 128k -c:s copy """{out}""" -y'
    elif scale == 360:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -c:v libx264 -pix_fmt yuv420p -preset faster -s 640x360 -crf 24 -c:a libopus -ac 2 -ab 128k -c:s copy """{out}""" -y'
    elif scale == 480:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -c:v libx264 -pix_fmt yuv420p -preset faster -s 854x480 -crf 24 -c:a libopus -ac 2 -ab 128k -c:s copy """{out}""" -y'
    elif scale == 720:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -c:v libx264 -pix_fmt yuv420p -preset faster -s 1280x720 -crf 24 -c:a libopus -ac 2 -ab 128k -c:s copy """{out}""" -y'
    try:
        await ffmpeg_progress(cmd, name, progress, FT, edit, ps_name, log=log)
    except Exception as e:
        await log.delete()
        await LOG_END(event, log_end_text)
        os.rmdir("encodemedia")
        print(e)
        return await edit.edit(f"**An Error Occured While FFMPEG Progress.\n\nContact :- [Star Bots Tamil Support]({SUPPORT_LINK})**", link_preview=False)  
    out2 = dt.now().isoformat("_", "seconds") + ".mp4" 
    if msg.file.name:
        out2 = msg.file.name
    else:
        out2 = dt.now().isoformat("_", "seconds") + ".mp4" 
    os.rename(out, out2)
    i_size = os.path.getsize(name)
    f_size = os.path.getsize(out2)     
    text = f'**{_ps}D By :- @{BOT_UN}\n\nBot 🤖 Channel :- [Star Bots Tamil](https://t.me/Star_Bots_Tamil)**'
    UT = time.time()
    await log.edit("Uploading file")
    if 'x-matroska' in mime:
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
            await Star_Bots_Tamil.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
        except Exception as e:
            await log.delete()
            await LOG_END(event, log_end_text)
            os.rmdir("encodemedia")
            print(e)
            return await edit.edit(f"**An Error Occured While Uploading.\n\nContact :- [Star Bots Tamil Support]({SUPPORT_LINK})**", link_preview=False)
    elif 'webm' in mime:
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
            await Star_Bots_Tamil.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
        except Exception as e:
            await log.delete()
            await LOG_END(event, log_end_text)
            os.rmdir("encodemedia")
            print(e)
            return await edit.edit(f"**An Error Occured While Uploading.\n\nContact :- [Star Bots Tamil Support]({SUPPORT_LINK})**", link_preview=False)
    else:
        metadata = video_metadata(out2)
        width = metadata["width"]
        height = metadata["height"]
        duration = metadata["duration"]
        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
            await Star_Bots_Tamil.send_file(event.chat_id, uploader, caption=text, thumb=JPG3, attributes=attributes, force_document=False)
        except Exception:
            try:
                uploader = await fast_upload(f'{out2}', f'{out2}', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
                await Star_Bots_Tamil.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
            except Exception as e:
                await log.delete()
                await LOG_END(event, log_end_text)
                os.rmdir("encodemedia")
                print(e)
                return await edit.edit(f"**An Error Occured While Uploading.\n\nContact :- [Star Bots Tamil Support]({SUPPORT_LINK})**", link_preview=False)
    await edit.delete()
    os.remove(name)
    os.remove(out2)
    await log.delete()
    log_end_text2 = f'**{_ps} Process Finished\n\nTime Taken :- {round((time.time()-DT)/60)} Minutes\nInitial Size :- {i_size/1000000}mb.\nFinal Size :- {f_size/1000000}mb.\n\n[Bot is Free Now]({SUPPORT_LINK})'
    await LOG_END(event, log_end_text2)
    
