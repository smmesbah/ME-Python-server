from pymongo import MongoClient

client = MongoClient('mongodb+srv://Samina:samina@cluster0.grz1bag.mongodb.net/')

db = client.User_db

collection_history = db["History_collections"]
collection_user = db["User_collection"]