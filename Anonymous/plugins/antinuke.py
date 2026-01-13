import time
import asyncio
from pyrogram import filters, enums
from pyrogram.types import ChatMemberUpdated
from Anonymous import app
from Anonymous.config import Config
from pymongo import MongoClient

# --- DATABASE CONNECTION ---
mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client["AnonymousDB"]
limits_col = db["admin_limits"]
auth_col = db["auth_users"]

# --- CONFIGURATION (LIMITS) ---
# Ek din me kitne allowed hain:
BAN_LIMIT = 3
KICK_LIMIT = 3
DEMOTE_LIMIT = 2

# --- HELPERS ---
def is_auth(chat_id, user_id):
    # Check if user is trusted (Auth List or Owner)
    return bool(auth_col.find_one({"chat_id": chat_id, "user_id": user_id}))

async def punish_admin(chat_id, user_id, action_type):
    try:
        # 1. Demote the Admin
        await app.promote_chat_member(
            chat_id, user_id,
            is_anonymous=False,
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_pin_messages=False
        )
        
        # 2. Send Alert
        user = await app.get_chat_member(chat_id, user_id)
        mention = user.user.mention
        await app.send_message(
            chat_id,
            f"🚨 **ANTI-NUKE ACTIVATED!**\n\n"
            f"👮‍♂️ **Rogue Admin:** {mention}\n"
            f"🛑 **Action:** Limit Exceeded ({action_type})\n"
            f"🔨 **Punishment:** Demoted immediately!"
        )
    except Exception as e:
        print(f"Punish Error: {e}")

# --- WATCHER: ADMIN ACTIONS ---
@app.on_chat_member_updated(group=99)
async def admin_action_watcher(client, message: ChatMemberUpdated):
    chat_id = message.chat.id
    
    # Humein sirf Ban/Kick/Demote dekhna hai
    if not (message.old_chat_member and message.new_chat_member): return
    
    # Actor kaun hai? (Jisne action liya)
    actor = message.from_user
    if not actor: return 
    
    # 1. Safety Checks
    # Agar Bot khud action le raha hai to ignore karo
    if actor.id == app.me.id: return
    # Agar Owner ya Auth User hai to ignore karo
    if is_auth(chat_id, actor.id) or actor.id in Config.OWNERS: return

    action = None
    
    # 2. Detect Action Type
    # Check for BAN (Member was member, now banned)
    if message.old_chat_member.status == enums.ChatMemberStatus.MEMBER and \
       message.new_chat_member.status == enums.ChatMemberStatus.BANNED:
        action = "ban"

    # Check for KICK (Member was member, now left/kicked)
    elif message.old_chat_member.status == enums.ChatMemberStatus.MEMBER and \
         message.new_chat_member.status == enums.ChatMemberStatus.LEFT:
        # Verify agar ye kick tha (Audit log check karna mushkil hai yahan, assume kick for safety)
        action = "kick"

    # Agar koi action detect nahi hua to return
    if not action: return

    # 3. Check Limits in Database
    current_time = time.time()
    record = limits_col.find_one({"chat_id": chat_id, "user_id": actor.id})

    if record:
        # Agar 24 ghante beet gaye hain, to limit reset karo
        if current_time > record['reset_time']:
            limits_col.update_one(
                {"_id": record['_id']},
                {"$set": {"ban_count": 0, "kick_count": 0, "reset_time": current_time + 86400}}
            )
            count = 1
        else:
            # Count badhao
            new_count = record.get(f"{action}_count", 0) + 1
            limits_col.update_one(
                {"_id": record['_id']},
                {"$set": {f"{action}_count": new_count}}
            )
            count = new_count
    else:
        # Naya record banao
        limits_col.insert_one({
            "chat_id": chat_id,
            "user_id": actor.id,
            "ban_count": 1 if action == "ban" else 0,
            "kick_count": 1 if action == "kick" else 0,
            "reset_time": current_time + 86400
        })
        count = 1

    # 4. Take Action if Limit Crossed
    limit = BAN_LIMIT if action == "ban" else KICK_LIMIT
    
    if count >= limit:
        await punish_admin(chat_id, actor.id, action)
        # Database se record uda do ya reset kar do taaki baar baar message na aaye
        limits_col.update_one({"chat_id": chat_id, "user_id": actor.id}, {"$set": {f"{action}_count": 0}})

# --- COMMAND: RESET LIMITS (Owner Only) ---
@app.on_message(filters.command("resetlimits") & filters.group)
async def reset_limits(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != enums.ChatMemberStatus.OWNER and message.from_user.id not in Config.OWNERS:
        return await message.reply("❌ Only Group Owner can reset limits.")
    
    limits_col.delete_many({"chat_id": message.chat.id})
    await message.reply("✅ **Anti-Nuke Limits Reset!**\nAll admins act clean now.")
  
