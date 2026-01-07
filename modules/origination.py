# modules/origination.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils.data_handler import save_loan
from utils.ai_model import risk_score, risk_label

class Origination(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Origination")

        layout = QVBoxLayout()

        title = QLabel("New Loan Application")
        title.setObjectName("title")
        layout.addWidget(title)

        self.name = QLineEdit()
        self.amount = QLineEdit()

        layout.addWidget(QLabel("Borrower Name"))
        layout.addWidget(self.name)

        layout.addWidget(QLabel("Loan Amount"))
        layout.addWidget(self.amount)

        btn = QPushButton("Submit Loan")
        btn.clicked.connect(self.submit)
        layout.addWidget(btn)

        self.setLayout(layout)

    def submit(self):
        borrower_name = self.name.text().strip()
        try:
            loan_amount = float(self.amount.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Error", "Loan amount must be a number")
            return

        score = risk_score(loan_amount)
        label = risk_label(score)

        # Create a single loan record
        loan = {
            "borrower": borrower_name,
            "amount": loan_amount,
            "risk_score": score,
            "risk_label": label
        }

        # Save directly to MongoDB
        save_loan(loan)

        QMessageBox.information(
            self,
            "AI Risk Assessment",
            f"Loan submitted!\nRisk Level: {label} ({score})"
        )

        # Clear input fields
        self.name.clear()
        self.amount.clear()
