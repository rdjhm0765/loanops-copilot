# modules/analytics.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from utils.data_handler import load_loans

class Analytics(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Analytics Dashboard")

        layout = QVBoxLayout()
        title = QLabel("Portfolio Analytics")
        title.setObjectName("title")
        layout.addWidget(title)

        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)

        self.setLayout(layout)
        self.refresh_stats()

    def refresh_stats(self):
        loans = load_loans()
        total_loans = len(loans)
        total_amount = sum(loan["amount"] for loan in loans) if loans else 0

        high_risk = len([loan for loan in loans if loan["risk_label"] == "High"])
        medium_risk = len([loan for loan in loans if loan["risk_label"] == "Medium"])
        low_risk = len([loan for loan in loans if loan["risk_label"] == "Low"])

        self.summary_label.setText(
            f"Total Loans: {total_loans}\n"
            f"Total Amount: ₹{total_amount}\n"
            f"High Risk: {high_risk} | Medium Risk: {medium_risk} | Low Risk: {low_risk}"
        )
