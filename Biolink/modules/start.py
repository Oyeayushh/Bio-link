import random
import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.enums import ChatType, ParseMode

from config import OWNER_ID, BOT_USERNAME
from Biolink import Biolink as app
from Biolink.helper.database import add_user, add_chat

# ─── Random Start Images ───────────────────────────────────────────────────────
START_IMAGES = [
    "https://files.catbox.moe/3w9hpn.jpg",
    "https://files.catbox.moe/ux6t07.jpg",
    "https://files.catbox.moe/k46ikf.jpg",
    "https://files.catbox.moe/9cqd3l.jpg",
    "https://files.catbox.moe/yqe7lh.jpg",
]

# ─── Animation Frames ──────────────────────────────────────────────────────────
LOADING_FRAMES = [
    "⬛⬛⬛⬛⬛",
    "🟥⬛⬛⬛⬛",
    "🟥🟧⬛⬛⬛",
    "🟥🟧🟨⬛⬛",
    "🟥🟧🟨🟩⬛",
    "🟥🟧🟨🟩🟦",
]

def get_random_image() -> str:
    return random.choice(START_IMAGES)

def get_start_caption(user):
    return f"""<b>ʜᴇʏ</b> {user.mention} 🥀

╔══════════════════╗
║  🤖 <b>ʙɪᴏʟɪɴᴋ ɢᴜᴀʀᴅ</b>  ║
╚══════════════════╝

🚫 <b>ᴡʜᴀᴛ ɪ ᴅᴏ :</b>
├ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs ᴡɪᴛʜ ʟɪɴᴋs
├ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴡɪᴛʜ ʙɪᴏʟɪɴᴋs
└ ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʟᴇᴀɴ ✨

<blockquote>⚡ <i>ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ɪ'ʟʟ ʜᴀɴᴅʟᴇ ᴛʜᴇ ʀᴇsᴛ!</i></blockquote>"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("✙ ᴧᴅᴅ ᴍᴇ ᴛσ ʏσᴜʀ ᴄʜᴧᴛ ✙", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [InlineKeyboardButton("🟢 ʜєʟᴘ ᴧηᴅ ᴄσϻϻᴧηᴅ", callback_data="show_help")],
    [
        InlineKeyboardButton("sυᴘᴘσʀᴛ", url="https://t.me/kanhaxduniya"),
        InlineKeyboardButton("υᴘᴅᴀᴛᴇ", url="https://t.me/about_kanhaa")
    ],
    [InlineKeyboardButton("ᴅᴇᴠᴇʟσᴘᴇʀ", url="https://t.me/Oyekanhaa")]
])

PRIVATE_START_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("• ᴘʀɪᴠᴀᴛᴇ ꜱᴛᴀʀᴛ •", url=f"https://t.me/{BOT_USERNAME}?start=help")]
])

@app.on_message(filters.command("start") & (filters.private | filters.group))
async def start_command(_, message: Message):
    user = message.from_user
    chat = message.chat

    await add_user(user.id)
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await add_chat(chat.id)

    if chat.type == ChatType.PRIVATE:
        # ── Animation: loading bar ──
        anim_msg = await message.reply_text(
            f"<b>⚡ ʟᴏᴀᴅɪɴɢ...</b>\n\n{LOADING_FRAMES[0]}",
            parse_mode=ParseMode.HTML
        )
        for frame in LOADING_FRAMES[1:]:
            await asyncio.sleep(0.3)
            try:
                await anim_msg.edit_text(
                    f"<b>⚡ ʟᴏᴀᴅɪɴɢ...</b>\n\n{frame}",
                    parse_mode=ParseMode.HTML
                )
            except:
                pass

        await asyncio.sleep(0.3)
        await anim_msg.delete()

        # ── Send random image with spoiler + copy protection ──
        await app.send_photo(
            chat_id=chat.id,
            photo=get_random_image(),
            caption=get_start_caption(user),
            parse_mode=ParseMode.HTML,
            has_spoiler=True,
            protect_content=True,
            reply_markup=START_BUTTONS
        )
    else:
        await message.reply_text(
            f"**ʜᴇʏ {user.mention}, ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ!**",
            reply_markup=PRIVATE_START_BUTTON
        )

@app.on_callback_query(filters.regex("^back_to_start$"))
async def back_to_start(_, query: CallbackQuery):
    user = query.from_user
    chat_id = query.message.chat.id

    await query.message.delete()

    await app.send_photo(
        chat_id=chat_id,
        photo=get_random_image(),
        caption=get_start_caption(user),
        parse_mode=ParseMode.HTML,
        has_spoiler=True,
        protect_content=True,
        reply_markup=START_BUTTONS
    )
