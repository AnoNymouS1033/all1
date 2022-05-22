import logging
logger = logging.getLogger(__name__)

from ..config import Config
from ..tools.text import TEXT
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


@Client.on_message(filters.command("help") & filters.private & filters.incoming)
async def help_user(c, m):
    button = [[
        InlineKeyboardButton('🏕️ Home', callback_data='back'),
        InlineKeyboardButton('💸 Donate', callback_data='donate')
        ],[
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await m.reply_text(
        text=TEXT.HELP_USER.format(m.from_user.first_name),
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )



@Client.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(c, m):
    start = await m.reply_text("**Checking...**", parse_mode="markdown", quote=True)

    button = [
        [
            InlineKeyboardButton('🧔 My Father', url='https://t.me/Ns_AnoNymous'),
            InlineKeyboardButton('📘 About', callback_data='about')
        ],
        [
            InlineKeyboardButton('💡 Help', callback_data="help"),
            InlineKeyboardButton('🛠 Settings', callback_data="setting")
        ],
        [
            InlineKeyboardButton('❌ Close', callback_data="close")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(button)
    await start.edit(
        text=TEXT.START_TEXT.format(m.from_user.first_name), 
        disable_web_page_preview=True,
        reply_markup=reply_markup
    ) 


@Client.on_message(filters.command("about") & filters.private & filters.incoming)
async def about(c, m):
    restart_time = Config.RESTART_TIME[0]
    time_format = restart_time.strftime("%d %B %Y %I:%M %p")
    button = [[
        InlineKeyboardButton('💡 Help', callback_data="help"),
        InlineKeyboardButton('💸 Donate', callback_data='donate')
        ],[
        InlineKeyboardButton('❌ Close', callback_data="close")
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await m.reply_text(
        text=TEXT.ABOUT.format(time_format),
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )


@Client.on_message(filters.command("set_caption") & filters.private & filters.incoming)
async def set_caption(c, m):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)

    if len(m.command) == 1:
        await m.reply_text(
            "Use this command to set the custom caption for your files."
            "For setting your caption send captin in the format \n`/set_caption <your_caption>`\n\n"
            "--**Examples:**--\n\n**Simple caption:** `/set_caption My caption`\n\n"
            "**Dynamic capiton:** `/set_caption 📕 File Name: {filename}\n\n💾 Size: {filesize}\n\n⏰ Duration: {duration}`\n\n\n"
            "--**Available Variables:**--\n\n"
            "    • `{filename}` - replaced by the filename\n"
            "    • `{duration}` - replaced by the duration of videos\n"
            "    • `{filesize}` - replaced by filesize\n\n"
            "**Note:**\n1. You can check the current caption using /caption\n"
            "2. This feature was inspired from @urluploadxbot",
            quote=True)
    else:
        if len(m.text.markdown) > len(m.text.html):
            caption = m.text.markdown.split(' ', 1)[1]
        else:
            caption = m.text.html.split(' ', 1)[1]
        await c.db.update_settings_status(m.from_user.id, 'custom_caption', caption)
        await m.reply_text(f'--**Your Caption:**--\n\n{caption}', quote=True)


@Client.on_message(filters.command("caption") & filters.private & filters.incoming)
async def caption(c, m):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)

    caption = await c.db.get_settings_status(m.from_user.id, 'custom_caption')
    if not caption:
        text = "You didn't set any custom caption yet for setting custom caption use /set_caption."
    else:
        text = f"--**Your custom caption:**-- \n\n{caption}"
    await m.reply_text(text, quote=True)


@Client.on_message(filters.command('list'))
async def list(c, m):
    result = Config.normal_queue._unfinished_tasks - len(Config.normal_queue._queue)
    ytdl = Config.queue._unfinished_tasks - len(Config.queue._queue)
    await m.reply_text(f'**--NORMAL UPLOAD SERVER:--**\n\n    •**Active Tasks:** {result}\n\n    •**Pending:** {len(Config.normal_queue._queue)}\n\n**--Ytdl Server:--**\n\n    •**Active Tasks:** {ytdl}\n\n    •**Pending:** {len(Config.queue._queue)}', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close ❌', callback_data='close')]]), quote=True)


@Client.on_message(filters.command("warn"))
async def warn(c, m):
    if m.from_user.id in Config.AUTH_USERS:
        if len(m.command) >= 3:
            try:
                user_id = m.text.split(' ', 2)[1]
                reason = m.text.split(' ', 2)[2]
                await m.reply_text("User Notfied Sucessfully")
                await c.send_message(chat_id=int(user_id), text=reason)
            except:
                 await m.reply_text("User not Notfied Sucessfully 😔")
    else:
        await m.reply_text(text="You are not admin 😡", quote=True)
