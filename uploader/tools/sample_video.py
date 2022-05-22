import logging
logger = logging.getLogger(__name__)

import os
import shutil
import time
import random
import asyncio
import concurrent.futures
from .take_screen_shot import take_screen_shot
from .get_duration import get_duration


async def generate_sample(location, c, m):
      try:
          send_message = await m.reply_text(text="Trying to generate sample video 📹", quote=True)

          # creating output directory 
          output_directory = f"./DOWNLOADS/{m.from_user.id}/{time.time()}"
          if not os.path.isdir(output_directory):
              os.makedirs(output_directory)

          # trying to get duration if Failed sending error message
          duration = await get_duration(location)
          if isinstance(duration, str):
              return await send_message.edit("**Hey, i am unable to generate sample video 😑**", parse_mode="markdown")

          # getting the starting and ending time of video
          reduced_sec = duration - int(duration * 10 / 100)
          sample_duration = await c.db.get_settings_status(m.from_user.id, 'sample_video')

          # stopping process if duration is less than sample video duration 
          if sample_duration > reduced_sec:
              return await send_message.edit("😒 Sorry i can't generate sample beacuse this **video duration** is less than **sample video duration**")

          start = random.randint(0, reduced_sec - sample_duration)
          end = start + sample_duration
          final_location = f"{output_directory}/Sample Video.mkv"

          # Trying to generate sample video if failes sending error message
          await send_message.edit("😎 **Generating Sample Video**", parse_mode="markdown")
          try:
              ffmpeg_cmd = [
                  "ffmpeg",
                  "-headers",
                  "IAM:",
                  "-hide_banner",
                  "-ss",
                  str(start),
                  "-i",
                  location,
                  "-t",
                  str(sample_duration),
                  "-map",
                  "0",
                  "-c",
                  "copy",
                  final_location,
              ]
              """loop = asyncio.get_event_loop()
              with concurrent.futures.ThreadPoolExecutor() as pool:
                  await loop.run_in_executor(pool, trim_video, location, start, end, final_location)"""
          except Exception as e:
              await m.reply_text(f"**Error:** {e}")
              await send_message.edit("**Unable to generate samplevideo 🤧**", parse_mode="markdown")

          await send_message.edit("**😤 Sample Video generated sucessfully.**\n\n__Now trying to upload__", parse_mode="markdown")
          duration = await get_duration(final_location)
          thumb_image_path = f"{output_directory}/{m.from_user.id}.jpg"
          try:
              thumb_image_path = await take_screen_shot(final_location, os.path.dirname(thumb_image_path), random.randint(0, duration - 1))
          except:
              thumb_image_path = None
          try:
              Video = await m.reply_video(
                  video=final_location,
                  duration=duration,
                  thumb=thumb_image_path,
                  caption="Sample Video",
                  supports_streaming=True
              )
              await send_message.delete()
              if Video is None:
                  await send_message.edit("**Upload failed!!**")
          except Exception as e:
              await send_message.edit(f"**Unable to upload sample video!!**\n\nReason: {e}", parse_mode="markdown")
          try:
              os.remove(final_location)
          except:
              pass

      except Exception as e:
          print(e)
          await send_message.edit(f"**Failed to generate sample video!!**\n\nDue some programming error. Report this issue in [Ns Bot Supporters](https://telegram.dog/Ns_Bot_supporters)", parse_mode="markdown", disable_web_page_preview=True)

def trim_video(location, start, end, final_location):
    ffmpeg_extract_subclip(location, start, end, targetname=final_location)
