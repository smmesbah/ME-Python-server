from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ["MONGO_URL"])

db = client.User_db

collection_history = db["History_collections"]
collection_user = db["User_collection"]
collection_todos = db["Todo_collection"]
collection_slack_access = db["Slack_access_collection"]
collection_slack_messages = db["Slack_messages_collection"]
# collection_history.create_index([("user_id", "token")])