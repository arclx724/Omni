import os
import aiohttp
import asyncio
from pyrogram import filters
from Anonymous import app
from Anonymous.config import Config
from pymongo import MongoClient

mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client["AnonymousDB"]
settings_col = db["security_settings"]
auth_col = db["auth_users"]

SIGHT_USER = getattr(Config, "SIGHT_USER", "")
SIGHT_SECRET = getattr(Config, "SIGHT_SECRET", "")

async def check_nsfw(file_path):
    url = 'https://api.sightengine.com/1.0/check.json'
    try:
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field('models', 'nudity')
            data.add_field('api_user', SIGHT_USER)
            data.add_field('api_secret', SIGHT_SECRET)
            data.add_field('media', open(file_path, 'rb'))
            async with session.post(url, data=data) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    if res['status'] == 'success' and (res['nudity']['raw'] > 0.60 or res['nudity']['partial'] > 0.70):
                        return True
    except: pass
    return False

@app.on_message((filters.photo | filters.video | filters.sticker) & filters.group, group=22)
async def media_watcher(client, message):
    st = settings_col.find_one({"chat_id": message.chat.id}) or {}
    if not st.get("imagefilter") or auth_col.find_one({"chat_id": message.chat.id, "user_id": message.from_user.id}): return

    try:
        file_path = await message.download()
        is_dirty = await check_nsfw(file_path)
        os.remove(file_path)

        if is_dirty:
            await message.delete()
            m = await message.reply(f"🚫 **NSFW Content Deleted!**\n👤 {message.from_user.mention}")
            await asyncio.sleep(60)
            await m.delete()
    except: pass
      
