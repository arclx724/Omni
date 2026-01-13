# (©) Anonymous Emperor

from pyrogram import filters

LOGS = -1002105665930

StartPic = [
    "https://telegra.ph/file/2aa827f56acf9dd6e2412.jpg",
    "https://telegra.ph/file/f8ce84ac828d47de1186b.jpg",
    "https://telegra.ph//file/77951e8914b2d07598dff.jpg",
    "https://telegra.ph/file/5927821703d2af33c0026.jpg",
    "https://telegra.ph/file/29beb52293e0659535556.jpg",
    "https://telegra.ph/file/ffc4e1cbbdaed22952aac.jpg",
    "https://telegra.ph/file/edb3f915d2ca31675c151.jpg",
    "https://telegra.ph/file/5efc878da21f053347e0c.jpg",
    "https://telegra.ph/file/02b12529db3e15422fdcc.jpg",
    "https://telegra.ph/file/232db3fccaac92015db3c.jpg",
    "https://telegra.ph/file/d7c7e0a4431d8e7650a70.jpg",
    "https://telegra.ph/file/c1b1f46f187a9ac452156.jpg",
    "https://telegra.ph/file/d70b8738afb7d55f9975d.jpg",
    "https://telegra.ph/file/76465fa10a6faf61a6953.jpg",
    "https://telegra.ph/file/4a869b17ad2fada9cb9bb.jpg",
    "https://telegra.ph/file/a602d475d8f9dcf52f814.jpg",
    "https://telegra.ph/file/bc6c146d78ca5f52f58d1.jpg",
    "https://telegra.ph/file/1655f876b5b96799f990e.jpg",
]

class Config:
    API_ID = 8042205941
    API_HASH = "fe300e4c648c0389a1d8ddd853ebccc1"
    BOT_TOKEN = "8238728169:AAF0oyGa5kBIrzfRP2v8AhJbfh2NIog23ds"
    TOKEN = BOT_TOKEN
    MONGO_URI = "mongodb+srv://arclx724_db_user:arclx724_db_user@cluster0.czhpczm.mongodb.net/?appName=Cluster0"
    OWNERS = [8042205941, 7432650544, 1284920298, 5907205317, 5881613383]
    DATABASE_NAME = "AnonymousDB"
    LOGS = -1002105665930
    SESSION = "STRING_SESSION"
    LOG_CHANNEL_ID = -1002105665930
    BOT_USERNAME = "MissBillieBot"
    PREFIX_HANDLER = ["/", "!", "toji ", "Toji "]
    BOT_NAME = "Toji • Fushiguro"
    OWNER_ID = 6346273488
    DEV_USERS = [5907205317, 5881613383, 1284920298, 1805959544, 8171988347]
    
    # --- New Keys (Inside Class) ---
    OPENROUTER_API_KEY = "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"
    SIGHT_USER = "222232214"
    SIGHT_SECRET = "3DHj7xorvBEZtPaLFJLwBP86L8qbzrN9"

# Global Variables
OWNER = 6346273488
DEVUSERS = [5907205317, 5881613383, 1284920298, 1805959544, 8171988347]
DEV_LEVEL = set(DEVUSERS + [int(OWNER)])
SUDOERS = filters.user()
BANNED_USERS = filters.user()
