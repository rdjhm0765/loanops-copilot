import json
import os
from datetime import datetime

SESSION_FILE = "data/.session.json"

class SessionManager:
    def __init__(self):
        self.session_data = self.load_session()
    
    def load_session(self):
        """Load existing session from file"""
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_session(self):
        """Save session to file"""
        os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
        with open(SESSION_FILE, 'w') as f:
            json.dump(self.session_data, f, indent=4)
    
    def create_session(self, username, role="user"):
        """Create a new session for a user"""
        self.session_data = {
            "username": username,
            "role": role,
            "login_time": datetime.now().isoformat(),
            "is_active": True
        }
        self.save_session()
    
    def get_current_user(self):
        """Get currently logged in user"""
        if self.session_data.get("is_active"):
            return self.session_data.get("username")
        return None
    
    def get_user_role(self):
        """Get role of current user"""
        if self.session_data.get("is_active"):
            return self.session_data.get("role")
        return None
    
    def is_authenticated(self):
        """Check if user is logged in"""
        return self.session_data.get("is_active", False)
    
    def logout(self):
        """End current session"""
        self.session_data["is_active"] = False
        self.session_data["logout_time"] = datetime.now().isoformat()
        self.save_session()
    
    def clear_session(self):
        """Clear session file"""
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        self.session_data = {}