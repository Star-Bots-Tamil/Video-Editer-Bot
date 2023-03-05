# (c) Star Bots Tamil

import os, subprocess, time

from datetime import datetime as dt
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from ethon.telefunc import fast_download, fast_upload
from ethon.pyfunc import bash, video_metadata
from ethon.pyutils import rename

from .. import BOT_UN

from Star-Bots-Tamil.localisation import SUPPORT_LINK, JPG, JPG2

async def mp3(event, msg):
    Star_Bots_Tamil = event.client
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0]
    else:
        out = dt.now().isoformat("_", "seconds")
    try:
        DT = time.time()
        await fast_download(name, file, Star_Bots_Tamil, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        bash(f"ffmpeg -i {name} -codec:a libmp3lame -q:a 0 {out}.mp3")
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}.mp3', f'{out}.mp3', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
        await Star_Bots_Tamil.send_file(event.chat_id, uploader, thumb=JPG, caption=f'**AUDIO EXTRACTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()
    os.remove(name)
    os.remove(f'{out}.mp3')                           
                       
async def flac(event, msg):
    Star_Bots_Tamil = event.client
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0]
    else:
        out = dt.now().isoformat("_", "seconds")
    try:
        DT = time.time()
        await fast_download(name, file, Star_Bots_Tamil, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        bash(f"ffmpeg -i {name} -codec:a libmp3lame -q:a 0 {out}.mp3")
        bash(f'ffmpeg -i {out}.mp3 -c:a flac {out}.flac')
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}.flac', f'{out}.flac', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
        await Star_Bots_Tamil.send_file(event.chat_id, uploader, thumb=JPG, caption=f'**AUDIO EXTRACTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()
    os.remove(name)
    os.remove(f'{out}.mp3')                           
    os.remove(f'{out}.flac')                 

async def wav(event, msg):
    Star_Bots_Tamil = event.client
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0]
    else:
        out = dt.now().isoformat("_", "seconds")
    try:
        DT = time.time()
        await fast_download(name, file, Star_Bots_Tamil, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        bash(f"ffmpeg -i {name} -codec:a libmp3lame -q:a 0 {out}.mp3")
        bash(f'ffmpeg -i {out}.mp3 {out}.wav')
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}.wav', f'{out}.wav', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
        await Star_Bots_Tamil.send_file(event.chat_id, uploader, thumb=JPG, caption=f'**AUDIO EXTRACTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()
    os.remove(name)
    os.remove(f'{out}.mp3')                           
    os.remove(f'{out}.wav')                 
                                       
async def mp4(event, msg):
    Star_Bots_Tamil = event.client
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0] 
    else:
        out = dt.now().isoformat("_", "seconds")
    try:
        DT = time.time()
        await fast_download(name, file, Star_Bots_Tamil, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        rename(name, f'{out}.mp4')
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}.mp4', f'{out}.mp4', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
        await Star_Bots_Tamil.send_file(event.chat_id, uploader, thumb=JPG, caption=f'**CONVERTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()                      
    os.remove(f'{out}.mp4')                 
                                           
async def mkv(event, msg):
    Star_Bots_Tamil = event.client
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0] + ".mkv"
    else:
        out = dt.now().isoformat("_", "seconds") + ".mkv"
    try:
        DT = time.time()
        await fast_download(name, file, Star_Bots_Tamil, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        rename(name, f'{out}')
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}', f'{out}', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
        await Star_Bots_Tamil.send_file(event.chat_id, uploader, thumb=JPG, caption=f'**CONVERTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()                        
    os.remove(f'{out}')
             
async def webm(event, msg):
    Star_Bots_Tamil = event.client
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0] + ".webm"
    else:
        out = dt.now().isoformat("_", "seconds") + ".webm"
    try:
        DT = time.time()
        await fast_download(name, file, Star_Bots_Tamil, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        rename(name, f'{out}')
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}', f'{out}', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
        await Star_Bots_Tamil.send_file(event.chat_id, uploader, thumb=JPG, caption=f'**CONVERTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()                 
    os.remove(f'{out}')
             
async def file(event, msg):
    Star_Bots_Tamil = event.client
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    try:
        DT = time.time()
        await fast_download(name, file, Star_Bots_Tamil, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{name}', f'{name}', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
        await Star_Bots_Tamil.send_file(event.chat_id, uploader, thumb=JPG, caption=f'**CONVERTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()
    os.remove(name)                           
    
async def video(event, msg):
    Star_Bots_Tamil = event.client
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0] + '.mp4'
    else:
        out = dt.now().isoformat("_", "seconds") + '.mp4'
    try:
        DT = time.time()
        await fast_download(name, file, Star_Bots_Tamil, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        rename(name, f'{out}')
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        metadata = video_metadata(out)
        width = metadata["width"]
        height = metadata["height"]
        duration = metadata["duration"]
        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]           
        UT = time.time()
        uploader = await fast_upload(f'{out}', f'{out}', UT, Star_Bots_Tamil, edit, '**UPLOADING:**')
        await Star_Bots_Tamil.send_file(event.chat_id, uploader, thumb=JPG2, caption=f'**CONVERTED by** : @{BOT_UN}', attributes=attributes, force_document=False)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()
    os.remove(out)                           
    
