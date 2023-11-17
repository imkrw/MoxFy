from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()


"""Put your own MongoDB Details"""
URI = os.getenv("MONGO_URI")
DB = os.getenv("DATABASE")
COLLECTION = os.getenv("COLLECTION")

client = MongoClient(URI)
db = client[DB]
collection = db[COLLECTION]

"""Find all documents in the collection"""
cursor = collection.find({}, {"_id": 0, "username": 1, "salt": 1, "password": 1})
