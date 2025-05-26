from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

cluster = MongoClient(os.environ.get("MONGO_URI"))
db = cluster["discord"]
collection = db["levelling"]

# Função para buscar ou criar documento de usuário
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

# Função para atualizar campos no documento do usuário
def update_user(user_id, guild_id, updates: dict):
    collection.update_one(
        {"user_id": str(user_id), "guild_id": str(guild_id)},
        {"$set": updates},
        upsert=True
    )