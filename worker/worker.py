import os
import time
import requests
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/socialdb")
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")

client = MongoClient(MONGO_URI)
db = client.get_database()
posts_collection = db.posts

def send_post(post):
    print(f"Sending post {post['_id']} to {post['platform']}: {post['content']}")
    posts_collection.update_one({"_id": post["_id"]}, {"$set": {"sent": True}})

while True:
    unsent_posts = list(posts_collection.find({"sent": False}))
    for post in unsent_posts:
        send_post(post)
    time.sleep(60)
