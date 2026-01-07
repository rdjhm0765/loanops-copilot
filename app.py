import sys
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication
from modules.auth import LoginWindow
from modules.dashboard import Dashboard
from utils.session import SessionManager

# Load environment variables
load_dotenv()

class App:
    def __init__(self):
        self.dashboard = None
        self.login = None
        self.session = SessionManager()
    
    def start(self):
        if self.session.is_authenticated():
            # Go directly to dashboard
            self.show_dashboard()
        else:
            # Show login window
            self.show_login()
    
    def show_login(self):
        self.login = LoginWindow()
        self.login.login_successful.connect(self.on_login_success)
        self.login.show()
    
    def on_login_success(self, username):
        print(f"Login successful for: {username}")
        self.show_dashboard()
    
    def show_dashboard(self):
        self.dashboard = Dashboard()
        self.dashboard.show()
        
        # Close login window if it exists
        if self.login:
            self.login.close()

def main():
    app = QApplication(sys.argv)

    # Load styles
    with open("ui/styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    # Create and start app
    main_app = App()
    main_app.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()