from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from utils.security import hash_password, verify_password
from utils.session import SessionManager
from utils.user_db import UserDatabase

class LoginWindow(QWidget):
    # Signal emitted when login succeeds
    login_successful = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LoanOps Copilot - Login")
        self.setFixedSize(400, 500)
        
        self.db = UserDatabase()
        self.session = SessionManager()
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo/Title
        title = QLabel("🔐 LoanOps Copilot")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("pageTitle")
        layout.addWidget(title)
        
        subtitle = QLabel("Secure Login")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Username
        username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.returnPressed.connect(self.login)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        
        # Login Button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)
        
        # Register link
        register_layout = QHBoxLayout()
        register_label = QLabel("Don't have an account?")
        register_btn = QPushButton("Register")
        register_btn.setObjectName("linkButton")
        register_btn.clicked.connect(self.show_register)
        register_layout.addWidget(register_label)
        register_layout.addWidget(register_btn)
        register_layout.addStretch()
        layout.addLayout(register_layout)
        
        layout.addStretch()
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        user = self.db.get_user(username)
        
        if user and verify_password(password, user['password_hash']):
            self.session.create_session(user['username'], user['role'])
            QMessageBox.information(self, "Success", f"Welcome back, {username}!")
            self.login_successful.emit(username)
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
            self.password_input.clear()
    
    def show_register(self):
        self.register_window = RegisterWindow(self.db)
        self.register_window.registration_successful.connect(self.on_registration_success)
        self.register_window.show()
    
    def on_registration_success(self, username):
        self.username_input.setText(username)
        QMessageBox.information(self, "Success", "Registration successful! Please login.")


class RegisterWindow(QWidget):
    registration_successful = pyqtSignal(str)
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Register New Account")
        self.setFixedSize(400, 550)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("Create Account")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("pageTitle")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Username
        username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Choose a strong password")
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        
        # Confirm Password
        confirm_label = QLabel("Confirm Password")
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setPlaceholderText("Re-enter your password")
        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_input)
        
        # Full Name
        name_label = QLabel("Full Name")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your full name")
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        
        # Register Button
        register_btn = QPushButton("Create Account")
        register_btn.clicked.connect(self.register)
        layout.addWidget(register_btn)
        
        layout.addStretch()
    
    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        fullname = self.name_input.text().strip()
        
        # Validation
        if not username or not password or not fullname:
            QMessageBox.warning(self, "Error", "All fields are required")
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, "Error", "Username must be at least 3 characters")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords don't match")
            return
        
        # Check if username exists
        if self.db.get_user(username):
            QMessageBox.warning(self, "Error", "Username already exists")
            return
        
        # Create user
        password_hash = hash_password(password)
        success = self.db.create_user(username, password_hash, fullname, "user")
        
        if success:
            self.registration_successful.emit(username)
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Registration failed. Please try again.")