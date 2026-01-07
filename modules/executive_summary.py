# modules/executive_summary.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from utils.data_handler import load_loans


class ExecutiveSummary(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Executive Summary")

        layout = QVBoxLayout(self)

        title = QLabel("Executive Risk Summary")
        title.setObjectName("title")
        layout.addWidget(title)

        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)

        self.refresh_summary()

    def refresh_summary(self):
        loans = load_loans()

        total_loans = len(loans)
        total_amount = sum(l["amount"] for l in loans) if loans else 0

        high_risk_loans = [l for l in loans if l["risk_label"] == "High"]
        medium_risk_loans = [l for l in loans if l["risk_label"] == "Medium"]

        high_risk_amount = sum(l["amount"] for l in high_risk_loans)
        medium_risk_amount = sum(l["amount"] for l in medium_risk_loans)

        if high_risk_amount > 0:
            recommendation = "Immediate monitoring required for high-risk loans."
        else:
            recommendation = "Portfolio risk is currently stable."

        self.summary_label.setText(
            f"Total Loans: {total_loans}\n"
            f"Total Portfolio Value: ₹{total_amount}\n\n"
            f"High Risk Loans: {len(high_risk_loans)}\n"
            f"Medium Risk Loans: {len(medium_risk_loans)}\n\n"
            f"₹ At Risk (High): ₹{high_risk_amount}\n"
            f"₹ Under Watch (Medium): ₹{medium_risk_amount}\n\n"
            f"Recommendation:\n{recommendation}"
        )
