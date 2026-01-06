from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils.data_handler import load_loans, save_loans
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
        score = risk_score(self.amount.text())
        label = risk_label(score)

        loans = load_loans()
        loans.append({
            "borrower": self.name.text(),
            "amount": self.amount.text(),
            "risk_score": score,
            "risk_label": label
        })
        save_loans(loans)

        QMessageBox.information(
            self,
            "AI Risk Assessment",
            f"Risk Level: {label} ({score})"
        )
