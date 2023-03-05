# (c) Star Bots Tamil

import asyncio, time, subprocess, re, os

from datetime import datetime as dt
from telethon import events
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from telethon.tl.types import DocumentAttributeVideo
from ethon.telefunc import fast_download, fast_upload
from ethon.pyfunc import video_metadata

from .. import Star_Bots_Tamil, BOT_UN, LOG_CHANNEL

from Star-Bots-Tamil.localisation import SUPPORT_LINK, JPG, JPG2, JPG3
from Star-Bots-Tamil.utils import ffmpeg_progress
from main.plugins.actions import LOG_START, LOG_END

async def compress(event, msg, ffmpeg_cmd=0, ps_name=None):
    if ps_name is None:
        ps_name = '**COMPRESSING:**'
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
    _ps = "COMPRESS"
    if ps_name != "**Compressing Your File 📂**":
        _ps = "ENCODE"
    log = await LOG_START(event, f'**{str(_ps)} Process Started\n\n[Bot is Busy Now]({SUPPORT_LINK})**')
    log_end_text = f'**{_ps} Process Finished\n\n[Bot is Free Now]({SUPPORT_LINK})**'
    try:
        await fast_download(n, file, Star_Bots_Tamil, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        os.rmdir("encodemedia")
        await log.delete()
        await LOG_END(event, log_end_text)
        print(e)
        return await edit.edit(f"An error occured while downloading.\n\nContact [SUPPORT]({SUPPORT_LINK})", link_preview=False) 
    name = '__' + dt.now().isoformat("_", "seconds") + ".mp4"
    os.rename(n, name)
    await edit.edit("**Extracting Metadata...**")
    vid = video_metadata(name)
    hgt = int(vid['height'])
    wdt = int(vid['width'])
    if ffmpeg_cmd == 2:
        if hgt == 360 or wdt == 640:
            await log.delete()
            await LOG_END(event, log_end_text)
            await edit.edit("**Fast Compress is Can't be Used for This Media File 📂, Try Using HEVC!**")
            os.rmdir("encodemedia")
            return
    FT = time.time()
    progress = f"progress-{FT}.txt"
    cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" None """{out}""" -y'
    if ffmpeg_cmd == 1:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -preset ultrafast -vcodec libx265 -crf 28 -acodec copy -c:s copy """{out}""" -y'
    elif ffmpeg_cmd == 2:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -c:v libx265 -crf 22 -preset ultrafast -s 640x360 -c:a copy -c:s copy """{out}""" -y'
    elif ffmpeg_cmd == 3:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -preset faster -vcodec libx265 -crf 22 -acodec copy -c:s copy """{out}""" -y'
    elif ffmpeg_cmd == 4:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -preset faster -vcodec libx264 -crf 22 -acodec copy -c:s copy """{out}""" -y'
    try:
        await ffmpeg_progress(cmd, name, progress, FT, edit, ps_name, log=log)
    except Exception as e:
        await log.delete()
        await LOG_END(event, log_end_text)
        os.rmdir("encodemedia")
        print(e)
        return await edit.edit(f"An error occured while FFMPEG progress.\n\nContact [SUPPORT]({SUPPORT_LINK})", link_preview=False)  
    out2 = dt.now().isoformat("_", "seconds") + ".mp4" 
    if msg.file.name:
        out2 = msg.file.name
    else:
        out2 = dt.now().isoformat("_", "seconds") + ".mp4" 
    os.rename(out, out2)
    i_size = os.path.getsize(name)
    f_size = os.path.getsize(out2)     
    text = F'**ENCODED by:** @{BOT_UN}'
    if ps_name != "**Encoding Your File 📂**":
        text = f'**Compressed by :- @{BOT_UN}\n\nBefore Compressing :- `{i_size}`\nAfter Compressing :- `{f_size}`\n\nBot 🤖 Channel :- [Star Bots Tamil](https://t.me/Star_Bots_Tamil)**'
    UT = time.time()
    await log.edit("Uploading file.")
    if 'x-matroska' in mime:
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Star_Bots_Tamil, edit, '**Uploading Your File 📂**')
            await Star_Bots_Tamil.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
        except Exception as e:
            await log.delete()
            await LOG_END(event, log_end_text)
            os.rmdir("encodemedia")
            print(e)
            return await edit.edit(f"**An Error Occured while Uploading.\n\nContact [SUPPORT]({SUPPORT_LINK})**", link_preview=False)
    elif 'webm' in mime:
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Star_Bots_Tamil, edit, '**Uploading Your File 📂**')
            await Star_Bots_Tamil.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
        except Exception as e:
            await log.delete()
            await LOG_END(event, log_end_text)
            os.rmdir("encodemedia")
            print(e)
            return await edit.edit(f"**An Error Occured while Uploading.\n\nContact [SUPPORT]({SUPPORT_LINK})**", link_preview=False)
    else:
        metadata = video_metadata(out2)
        width = metadata["width"]
        height = metadata["height"]
        duration = metadata["duration"]
        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Star_Bots_Tamil, edit, '**Uploading Your File 📂**')
            await Star_Bots_Tamil.send_file(event.chat_id, uploader, caption=text, thumb=JPG3, attributes=attributes, force_document=False)
        except Exception:
            try:
                uploader = await fast_upload(f'{out2}', f'{out2}', UT, Star_Bots_Tamil, edit, '**Uploading Your File 📂**')
                await Star_Bots_Tamil.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
            except Exception as e:
                await log.delete()
                await LOG_END(event, log_end_text)
                os.rmdir("encodemedia")
                print(e)
                return await edit.edit(f"**An Error Occured while Uploading.\n\nContact [SUPPORT]({SUPPORT_LINK})**", link_preview=False)
    await edit.delete()
    os.remove(name)
    os.remove(out2)
    await log.delete()
    log_end_text2 = f'**{_ps} Process Finished\n\nTime Taken :- {round((time.time()-DT)/60)} Minutes\nInitial Size :- {i_size/1000000}mb.\nFinal Size :- {f_size/1000000}mb.\n\n[Bot is Free Now.]({SUPPORT_LINK})**'
    await LOG_END(event, log_end_text2)
    


