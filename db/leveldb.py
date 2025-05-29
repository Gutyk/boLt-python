from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER")
MONGO_APP = os.environ.get("MONGO_APP")

MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUSTER}.mongodb.net/"
    f"?retryWrites=true&w=majority&appName={MONGO_APP}"
)


cluster = MongoClient(os.environ.get(MONGO_URI))
db = cluster["discord"]
collection = db["levelling"]

def get_user_document(user_id, guild_id):
    doc = collection.find_one({"user_id": str(user_id), "guild_id": str(guild_id)})
    if not doc:
        doc = {
            "user_id": str(user_id),
            "guild_id": str(guild_id),
            "xp": 0,
            "coins": 0,
            "last_daily": None,
        }
        collection.insert_one(doc)
    return doc

def update_user(user_id, guild_id, updates: dict):
    collection.update_one(
        {"user_id": str(user_id), "guild_id": str(guild_id)},
        {"$set": updates},
        upsert=True
    )