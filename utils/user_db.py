# utils/userdb.py

from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
from datetime import datetime
from utils.security import hash_password, verify_password

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_col = db["users"]

class UserDatabase:
    def get_user(self, username):
        return users_col.find_one({"username": username}, {"_id": 0})

    def create_user(self, username, password_hash, fullname, role="user"):
        if self.get_user(username):
            return False
        new_user = {
            "username": username,
            "password_hash": password_hash,
            "fullname": fullname,
            "role": role,
            "created_at": datetime.now().isoformat()
        }
        users_col.insert_one(new_user)
        return True

    def update_user(self, username, **kwargs):
        result = users_col.update_one(
            {"username": username},
            {"$set": kwargs}
        )
        return result.modified_count > 0

    def delete_user(self, username):
        users_col.delete_one({"username": username})
        return True
