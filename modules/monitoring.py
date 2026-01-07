# modules/monitoring.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
from utils.data_handler import load_loans

class Monitoring(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Monitoring")

        layout = QVBoxLayout()
        title = QLabel("Loan Risk Monitoring")
        title.setObjectName("title")
        layout.addWidget(title)

        self.loan_list = QListWidget()
        layout.addWidget(self.loan_list)

        self.setLayout(layout)
        self.refresh_loans()

    def refresh_loans(self):
        self.loan_list.clear()
        loans = load_loans()
        for loan in loans:
            self.loan_list.addItem(
                f"{loan['borrower']}: ₹{loan['amount']} | Risk: {loan['risk_label']} ({loan['risk_score']})"
            )
