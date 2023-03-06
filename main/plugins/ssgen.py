# (c) Star Bots Tamil

import os, time, subprocess, asyncio

from datetime import datetime as dt
from telethon import events
from . import fast_download
from ethon.pyfunc import video_metadata

def hhmmss(seconds):
    x = time.strftime('%H:%M:%S',time.gmtime(seconds))
    return x

async def ssgen(video, time_stamp):
    out = dt.now().isoformat("_", "seconds") + ".jpg"
    cmd = ["ffmpeg",
           "-ss",
           f"{hhmmss(time_stamp)}", 
           "-i",
           f"{video}",
           "-frames:v",
           "1", 
           f"{out}",
           "-y"
          ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
        
    stdout, stderr = await process.communicate()
    x = stderr.decode().strip()
    y = stdout.decode().strip()
    if os.path.isfile(out):
        return out
    else:
        None       
        
async def screenshot(event, msg):
    Star_Bots_Tamil = event.client
    name = dt.now().isoformat("_", "seconds") + ".mp4"
    edit = await Star_Bots_Tamil.send_message(event.chat_id, "**Trying to Process.**", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    if msg.file.name:
        name = msg.file.name
    try:
        await fast_download(name, file, Star_Bots_Tamil, edit, time.time(), "**Downloading Your File 📂**")
    except Exception as e:
        print(e)
        return await edit.edit(f"**An Error Occured While Downloading.**") 
    pictures = []
    captions = []
    n = [8, 7, 6, 5, 4, 3, 2, 1.5, 1.25, 1.10]
    duration = (video_metadata(name))["duration"]
    for i in range(10):
        sshot = await ssgen(name, duration/n[i]) 
        if sshot is not None:
            pictures.append(sshot)
            captions.append(f'**Screenshot at {hhmmss(duration/n[i])}**')
            await edit.edit(f"**`{i+1}` Screenshots Generated.**")
    if len(pictures) > 0:
        await Star_Bots_Tamil.send_file(event.chat_id, pictures, caption=captions)
    else:
        await edit.edit("**No Screenshots Could be Generated!**")
    await edit.delete()
    try:
        for pic in pictures:
             os.remove(pic)
        os.remove(name)
    except Exception:
        pass
