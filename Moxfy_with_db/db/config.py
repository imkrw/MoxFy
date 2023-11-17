from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

URI = os.getenv("MONGO_URI")
DB = os.getenv("DATABASE")
COLLECTION = os.getenv("COLLECTION")
client = MongoClient(URI, tlsCAFile=certifi.where())
db = client[DB]
collection = db[COLLECTION]
