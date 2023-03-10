# (c) Star Bots Tamil

import time, os

from datetime import datetime as dt
from telethon import events
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from telethon.tl.types import DocumentAttributeVideo
from ethon.telefunc import fast_download, fast_upload
from ethon.pyfunc import video_metadata, bash
from ethon.pyutils import rename

from .. import Star_Bots_Tamil, BOT_UN

from StarBotsTamil.presents import SUPPORT_LINK, JPG, JPG2, JPG3

async def trim(event, msg, st, et):
    Star_Bots_Tamil = event.client
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "**Trying to Process.**", reply_to=msg.id)
    new_name = "out_" + dt.now().isoformat("_", "seconds")
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    mime = msg.file.mime_type
    if 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
        out = new_name + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
        out = new_name + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
        out = new_name + ".mkv"       
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm" 
        out = new_name + ".webm"
    else:
        name = msg.file.name
        ext = (name.split("."))[1]
        out = new_name + ext
    DT = time.time()
    try:
        await fast_download(name, file, Star_Bots_Tamil, edit, DT, "**Downloading Your File 📂**")
    except Exception as e:
        print(e)
        return await edit.edit(f"**An Error Occured While Downloading.\n\nContact :- [Star Bots Tamil Support]({SUPPORT_LINK})**", link_preview=False) 
    try:
        await edit.edit("**Trimming Your File 📂**")
        bash(f'ffmpeg -i {name} -ss {st} -to {et} -acodec copy -vcodec copy {out}')
        out2 = new_name + '_2_' + '.mp4'
        rename(out, out2)
    except Exception as e:
        print(e)
        return await edit.edit(f"**An Error Occured While Trimming!\n\nContact :- [Star Bots Tamil Support]({SUPPORT_LINK})**", link_preview=False)
    UT = time.time()
    text = f"**Trimmed By :- @{BOT_UN}**"
    try:
        metadata = video_metadata(out2)
        width = metadata["width"]
        height = metadata["height"]
        duration = metadata["duration"]
        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
        uploader = await fast_upload(f'{out2}', f'{out2}', UT, Star_Bots_Tamil, edit, '**Uploading Your File 📂**')
        await Star_Bots_Tamil.send_file(event.chat_id, uploader, caption=text, thumb=JPG3, attributes=attributes, force_document=False)
    except Exception:
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Star_Bots_Tamil, edit, '**Uploading  Your File 📂**')
            await Star_Bots_Tamil.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
        except Exception as e:
            print(e)
            return await edit.edit(f"**An Error Occured While Uploading.\n\nContact :- [Star Bots Tamil Support]({SUPPORT_LINK})", link_preview=False)
    await edit.delete()
    os.remove(name)
    os.remove(out2)
      
      
      
      
