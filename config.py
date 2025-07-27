from pymongo import MongoClient
import os

MONGODB_URI = os.getenv("MONGODB_URI", "")

# MongoDB se credentials fetch karna
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client["filestorebot"]
config = db["variables"].find_one() or {}
inserted_config = db["userinfo"]


API_ID = os.getenv("API_ID", '') or config.get("API_ID", '')
API_HASH = os.getenv("API_HASH", '') or config.get("API_HASH", '')
BOT_TOKEN = os.getenv("BOT_TOKEN", '') or config.get("BOT_TOKEN", '')
OWNER_ID = os.getenv("OWNER_ID", '') or config.get("OWNER_ID", '')
BOT_USERNAME = os.getenv("BOT_USERNAME", '') or config.get("BOT_USERNAME", '')
STORAGE_CHANNEL_ID = os.getenv("STORAGE_CHANNEL_ID", '') or config.get("STORAGE_CHANNEL_ID", '')