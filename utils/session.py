# utils/session.py

from datetime import datetime

class SessionManager:
    _session = {}

    def create_session(self, username, role="user"):
        SessionManager._session = {
            "username": username,
            "role": role,
            "login_time": datetime.utcnow(),
            "is_active": True
        }

    def is_authenticated(self):
        return SessionManager._session.get("is_active", False)

    def get_current_user(self):
        return SessionManager._session.get("username")

    def get_user_role(self):
        return SessionManager._session.get("role")

    def logout(self):
        SessionManager._session.clear()
