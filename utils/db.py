import json
import os

USERS_FILE = "data/users.json"

class UserDatabase:
    def __init__(self):
        self.users_file = USERS_FILE
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Create users file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump([], f)
    
    def load_users(self):
        """Load all users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_users(self, users):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)
    
    def get_user(self, username):
        """Get user by username"""
        users = self.load_users()
        for user in users:
            if user['username'] == username:
                return user
        return None
    
    def create_user(self, username, password_hash, fullname, role="user"):
        """Create a new user"""
        users = self.load_users()
        
        # Check if username already exists
        if any(u['username'] == username for u in users):
            return False
        
        new_user = {
            "username": username,
            "password_hash": password_hash,
            "fullname": fullname,
            "role": role,
            "created_at": str(datetime.now())
        }
        
        users.append(new_user)
        self.save_users(users)
        return True
    
    def update_user(self, username, **kwargs):
        """Update user information"""
        users = self.load_users()
        
        for user in users:
            if user['username'] == username:
                user.update(kwargs)
                self.save_users(users)
                return True
        
        return False
    
    def delete_user(self, username):
        """Delete a user"""
        users = self.load_users()
        users = [u for u in users if u['username'] != username]
        self.save_users(users)
        return True

from datetime import datetime