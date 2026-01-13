import aiohttp
import asyncio
from pyrogram import filters
from Anonymous import app
from Anonymous.config import Config
from pymongo import MongoClient
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Database & Config
mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client["AnonymousDB"]
settings_col = db["security_settings"]
auth_col = db["auth_users"]
API_KEY = getattr(Config, "OPENROUTER_API_KEY", "")

# Helper Functions
def get_settings(chat_id):
    return settings_col.find_one({"chat_id": chat_id}) or {}

def is_auth(chat_id, user_id):
    return bool(auth_col.find_one({"chat_id": chat_id, "user_id": user_id}))

async def check_ai_profanity(text):
    if not text or len(text) < 2: return False, text
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    prompt = (f"Check for profanity (Hindi/English/Hinglish): '{text}'. "
              "If abusive, REWRITE wrapping ONLY bad words in ||word||. Else return 'SAFE'.")
    data = {"model": "google/gemini-2.0-flash-001", "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    result = res['choices'][0]['message']['content'].strip()
                    if "SAFE" not in result: return True, result
    except: pass
    return False, text

# Main Filter
@app.on_message((filters.text | filters.caption) & filters.group, group=20)
async def profanity_watcher(client, message):
    st = get_settings(message.chat.id)
    if not st.get("profanity") or is_auth(message.chat.id, message.from_user.id): return

    is_bad, censored_text = await check_ai_profanity(message.text or message.caption)
    if is_bad:
        try:
            await message.delete()
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Updates", url="https://t.me/DevilsHeavenMF")]])
            m = await message.reply(f"🤐 **{message.from_user.mention} said:**\n\n{censored_text}", reply_markup=btn)
            await asyncio.sleep(60)
            await m.delete()
        except: pass
          
