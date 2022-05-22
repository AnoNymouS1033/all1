import logging
logger = logging.getLogger(__name__)

import os
import time 
import aria2p
import asyncio
import subprocess

from math import floor
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def starting_aria2():
    cmd = [
        "aria2c",
        "--daemon=true",
        "--enable-rpc",
        "--follow-torrent=mem",
        "--max-connection-per-server=10",
        "--max-concurrent-downloads=20",
        "--max-tries=3",
        "--min-split-size=10M",
        "--rpc-listen-all=false",
        "--rpc-listen-port=6800",
        "--rpc-max-request-size=1024M",
        "--seed-time=0",
        "--split=10",
        "--bt-stop-timeout=0"
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=6800,
            secret=""
        )
    )
    return aria2


async def download_url(aria2, gid, event, start):
    while True:
        try:
            file = aria2.get_download(gid)
            if time.time() - start < 1800:
                complete = file.is_complete
                if not complete:
                    if not file.error_message:
                        block = ""
                        for i in range(1, 11):
                            if i <= floor(file.progress * 10 / 100):
                                block += '■'
                            else:
                                block += '□'
 
                        msg = f"**𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀:** {file.progress_string()}\n"
                        msg += f"[{block}]"
                        msg += f"\n\n🔰 **Speed:** `{file.download_speed_string()}`"
                        msg += f"\n\n✔ **Done ✔:** `{file.completed_length_string()}`"
                        msg += f"\n\n💾 **Total:** `{file.total_length_string()}`"
                        msg += f"\n\n⏰ **Time Left:** `{file.eta_string()}`"

                        button = [[InlineKeyboardButton('𝖢𝖺𝗇𝖼𝖾𝗅 ❌', callback_data=f'cancel_gid+{gid}')]]
                        try:
                            await event.edit(text=msg, parse_mode="markdown", reply_markup=InlineKeyboardMarkup(button))
                            await asyncio.sleep(3)
                        except:
                            pass
                    else:
                        msg = file.error_message
                        await event.edit(f"`{msg}`")
                        return False
                else:
                    await event.edit(f"**File Name:** __{file.name}__\n\n**Downloaded Successfully**")
                    return True
            else:
                file.remove(force=True)
                await event.edit("Download Auto Cancelled bue to **timeout**", parse_mode="markdown")
                return False
        except Exception as e:
            if " not found" in str(e) or "file" in str(e):
                await event.edit(f"__Process Cancelled Successfully ✅__", parse_mode="markdown")
                return False
            elif " depth exceeded" in str(e):
                file.remove(force=True)
                await event.edit(f"**Download Auto Canceled :**\n`{file.name}`\nYour Torrent/Link is Dead.")
                return False
            else:
                print(e)
                await event.edit("<u>error</u> :\n<code>{}</code> \n\n".format(str(e)))
                return False
