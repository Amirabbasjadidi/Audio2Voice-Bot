from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, Message
from pyrogram.errors import UserNotParticipant
import os
import asyncio
import subprocess
from datetime import datetime, timezone
from languages import en, fa, es, ru, zh, ar, de, it, tr, fr, ja, ko, hi, pt, hu, ro, nl, sv
import json

api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"
app = Client("voice_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Example: FFMPEG_PATH = "C:\\path\\to\\your\\ffmpeg\\bin\\ffmpeg.exe"
FFMPEG_PATH = None

# Maximum file size in bytes (50 MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

CHANNEL_USERNAME = "@amirabbas_jadidi"


user_languages = {}
if os.path.exists("user_languages.json"):
    with open("user_languages.json", "r") as f:
        user_languages = json.load(f)

def save_user_languages():
    with open("user_languages.json", "w") as f:
        json.dump(user_languages, f)

def get_message(user_id, message_key):
    lang = user_languages.get(str(user_id), "en")
    if lang == "fa":
        return fa.messages[message_key]
    elif lang == "es":
        return es.messages[message_key]
    elif lang == "ru":
        return ru.messages[message_key]
    elif lang == "zh":
        return zh.messages[message_key]
    elif lang == "ar":
        return ar.messages[message_key]
    elif lang == "de":
        return de.messages[message_key]
    elif lang == "it":
        return it.messages[message_key]
    elif lang == "tr":
        return tr.messages[message_key]
    elif lang == "fr":
        return fr.messages[message_key]
    elif lang == "ja":
        return ja.messages[message_key]
    elif lang == "ko":
        return ko.messages[message_key]
    elif lang == "hi":
        return hi.messages[message_key]
    elif lang == "pt":
        return pt.messages[message_key]
    elif lang == "hu":
        return hu.messages[message_key]
    elif lang == "ro":
        return ro.messages[message_key]
    elif lang == "nl":
        return nl.messages[message_key]
    elif lang == "sv":
        return sv.messages[message_key]
    else:
        return en.messages[message_key]

async def is_user_member(client, user_id):
    try:
        await client.get_chat_member(CHANNEL_USERNAME, user_id)
        return True
    except UserNotParticipant:
        return False

async def update_progress(message: Message, progress: int, status_message: str):
    progress_bar = "[" + "█" * (progress // 10) + " " * (10 - progress // 10) + "]"
    await message.edit_text(f"{status_message}\n{progress_bar} {progress}%")

async def download_with_progress(message, file_info):
    user_id = message.from_user.id
    file_name = f"{file_info.file_name.rsplit('.', 1)[0]}_{user_id}_{int(datetime.now().timestamp())}.{file_info.file_name.rsplit('.', 1)[-1]}"
    progress_message = await message.reply_text(get_message(user_id, "downloading"))

    def progress(current, total):
        percent = int(current * 100 / total)
        asyncio.run_coroutine_threadsafe(
            update_progress(progress_message, percent, get_message(user_id, "downloading")),
            app.loop
        )

    input_file = await message.download(file_name=file_name, progress=progress)

    if input_file:
        await progress_message.edit_text(get_message(user_id, "converting"))

    return input_file, progress_message

async def upload_with_progress(client, message, output_file):
    user_id = message.from_user.id
    progress_message = await message.reply_text(get_message(user_id, "uploading"))

    file_size = os.path.getsize(output_file)

    def progress(current, total):
        percent = int(current * 100 / total)
        asyncio.run_coroutine_threadsafe(
            update_progress(progress_message, percent, get_message(user_id, "uploading")),
            app.loop
        )

    with open(output_file, "rb") as f:
        await client.send_voice(message.chat.id, f, progress=progress)

    await progress_message.delete()

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    if str(user_id) not in user_languages:
        language_buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🇮🇷فارسی", callback_data="fa"), InlineKeyboardButton("English🇺🇸", callback_data="en")],
                [InlineKeyboardButton("Español🇪🇦", callback_data="es"), InlineKeyboardButton("Русский🇷🇺", callback_data="ru")],
                [InlineKeyboardButton("中文🇨🇳", callback_data="zh"), InlineKeyboardButton("العربية🇸🇦", callback_data="ar")],
                [InlineKeyboardButton("Deutsch🇩🇪", callback_data="de"), InlineKeyboardButton("Italiano🇮🇹", callback_data="it")],
                [InlineKeyboardButton("Türkçe🇹🇷", callback_data="tr"), InlineKeyboardButton("Français🇫🇷", callback_data="fr")],
                [InlineKeyboardButton("日本語🇯🇵", callback_data="ja"), InlineKeyboardButton("한국어🇰🇷", callback_data="ko")],
                [InlineKeyboardButton("हिंदी🇮🇳", callback_data="hi"), InlineKeyboardButton("Português🇵🇹", callback_data="pt")],
                [InlineKeyboardButton("Magyar🇭🇺", callback_data="hu"), InlineKeyboardButton("Română🇷🇴", callback_data="ro")],
                [InlineKeyboardButton("Nederlands🇳🇱", callback_data="nl"), InlineKeyboardButton("Svenska🇸🇪", callback_data="sv")]
            ]
        )
        await message.reply_text(
            get_message(user_id, "choose_language"),
            reply_markup=language_buttons
        )
    else:
        await message.reply_text(get_message(user_id, "start"))
    await client.set_bot_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("lang", "Change language")
    ])

@app.on_callback_query(filters.regex("^(fa|en|es|ru|zh|ar|de|it|tr|fr|ja|ko|hi|pt|hu|ro|nl|sv)$"))
async def set_language(client, callback_query):
    user_id = callback_query.from_user.id
    chosen_language = callback_query.data
    user_languages[str(user_id)] = chosen_language
    save_user_languages()
    await callback_query.message.delete()
    await callback_query.message.reply_text(get_message(user_id, "start"))
    await callback_query.answer()

@app.on_message(filters.command("lang"))
async def change_language(client, message):
    user_id = message.from_user.id
    language_buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🇮🇷فارسی", callback_data="fa"), InlineKeyboardButton("English🇺🇸", callback_data="en")],
            [InlineKeyboardButton("Español🇪🇦", callback_data="es"), InlineKeyboardButton("Русский🇷🇺", callback_data="ru")],
            [InlineKeyboardButton("中文🇨🇳", callback_data="zh"), InlineKeyboardButton("العربية🇸🇦", callback_data="ar")],
            [InlineKeyboardButton("Deutsch🇩🇪", callback_data="de"), InlineKeyboardButton("Italiano🇮🇹", callback_data="it")],
            [InlineKeyboardButton("Türkçe🇹🇷", callback_data="tr"), InlineKeyboardButton("Français🇫🇷", callback_data="fr")],
            [InlineKeyboardButton("日本語🇯🇵", callback_data="ja"), InlineKeyboardButton("한국어🇰🇷", callback_data="ko")],
            [InlineKeyboardButton("हिंदी🇮🇳", callback_data="hi"), InlineKeyboardButton("Português🇵🇹", callback_data="pt")],
            [InlineKeyboardButton("Magyar🇭🇺", callback_data="hu"), InlineKeyboardButton("Română🇷🇴", callback_data="ro")],
            [InlineKeyboardButton("Nederlands🇳🇱", callback_data="nl"), InlineKeyboardButton("Svenska🇸🇪", callback_data="sv")]
        ]
    )
    await message.reply_text(
        get_message(user_id, "choose_language"),
        reply_markup=language_buttons
    )

@app.on_message(filters.document | filters.audio | filters.voice)
async def handle_audio(client, message):
    user_id = message.from_user.id
    file_info = None
    if message.document:
        file_info = message.document
    if message.audio:
        file_info = message.audio
    elif message.voice:
        file_info = message.voice

    if not await is_user_member(client, user_id):
        join_buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(get_message(user_id, "join_channel"), url=f"https://t.me/{CHANNEL_USERNAME[1]}")],
                [InlineKeyboardButton(get_message(user_id, "check_membership"), callback_data="check_membership")]
            ]
        )
        await message.reply_text(get_message(user_id, "must_join"), reply_markup=join_buttons)
        return

    if file_info:
        valid_mime_types = [
            "audio/ogg",
            "audio/vorbis",
            "audio/x-vorbis+ogg",
            "audio/mpeg",
            "audio/wav",
            "audio/x-wav",
            "audio/vnd.wave"
        ]
        if file_info.mime_type in valid_mime_types:
            if file_info.file_size <= MAX_FILE_SIZE:
                start_time = datetime.now()

                input_file, progress_message = await download_with_progress(message, file_info)

                if input_file:
                    status_message = get_message(user_id, "converting")
                    for i in range(0, 101, 10):
                        await asyncio.sleep(0.5)
                        await update_progress(progress_message, i, status_message)

                    output_file = input_file.rsplit(".", 1)[0] + "_converted.ogg"
                    try:
                        subprocess.run(
                            [FFMPEG_PATH if FFMPEG_PATH else 'ffmpeg', "-i", input_file, "-c:a", "libopus", output_file],
                            check=True
                        )

                        await upload_with_progress(client, message, output_file)

                        end_time = datetime.now()
                        total_time = end_time - start_time
                        total_seconds = int(total_time.total_seconds())
                        formatted_time = str(datetime.fromtimestamp(total_seconds, timezone.utc).strftime('%H:%M:%S'))
                        await progress_message.edit_text(
                            f"{get_message(user_id, 'success')}\n"
                            f"{get_message(user_id, 'start_time')}: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                            f"{get_message(user_id, 'end_time')}: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                            f"{get_message(user_id, 'total_time')}: {formatted_time}\n"
                            f"{get_message(user_id, 'voice_sent')}"
                        )
                        os.remove(input_file)
                        os.remove(output_file)
                    except Exception as e:
                        await message.reply_text(get_message(user_id, 'error_conversion'))
                else:
                    await progress_message.delete()
                    await message.reply_text(get_message(user_id, 'error_download'))
            else:
                await message.reply_text(get_message(user_id, 'file_too_large'))
        else:
            await message.reply_text(get_message(user_id, 'invalid_file'))
    else:
        await message.reply_text(get_message(user_id, 'invalid_file'))

@app.on_callback_query(filters.regex("^check_membership$"))
async def check_membership(client, callback_query):
    user_id = callback_query.from_user.id
    if await is_user_member(client, user_id):
        await callback_query.message.delete()
        await callback_query.message.reply_text(get_message(user_id, "join_message"))
        await callback_query.answer()
    else:
        await callback_query.answer(get_message(user_id, "not_member"), show_alert=True)

app.run()
