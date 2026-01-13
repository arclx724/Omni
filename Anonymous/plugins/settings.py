from pyrogram import filters, enums
from Anonymous import app
from Anonymous.config import Config
from pymongo import MongoClient

mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client["AnonymousDB"]
settings_col = db["security_settings"]
auth_col = db["auth_users"]

async def check_admin(message):
    try:
        mem = await message.chat.get_member(message.from_user.id)
        return mem.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    except: return False

@app.on_message(filters.command(["profanity", "noedit", "imagefilter"]) & filters.group)
async def toggle_features(client, message):
    if not await check_admin(message): return
    if len(message.command) < 2: return await message.reply("Usage: `/command on` or `off`")
    
    cmd = message.command[0].lower()
    state = message.command[1].lower() == "on"
    settings_col.update_one({"chat_id": message.chat.id}, {"$set": {cmd: state}}, upsert=True)
    await message.reply(f"✅ **{cmd.capitalize()}** is now **{'ENABLED' if state else 'DISABLED'}**.")

@app.on_message(filters.command("auth") & filters.group)
async def authorize_user(client, message):
    if not await check_admin(message): return
    if not message.reply_to_message: return await message.reply("Reply to user.")
    
    user = message.reply_to_message.from_user
    auth_col.update_one({"chat_id": message.chat.id, "user_id": user.id}, {"$set": {"auth": True}}, upsert=True)
    await message.reply(f"✅ Authorized {user.mention}.")

