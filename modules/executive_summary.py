from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
import json
import os

DATA_FILE = "sample_loans.json"

class ExecutiveSummary(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Executive Summary")
        self.setMinimumSize(900, 600)
        self.init_ui()

    def load_loans(self):
        if not os.path.exists(DATA_FILE):
            return []

        with open(DATA_FILE, "r") as f:
            return json.load(f)

    def init_ui(self):
        loans = self.load_loans()

        total_loans = len(loans)
        high_risk = sum(1 for l in loans if l.get("risk_label") == "High")
        avg_risk = round(
            sum(l.get("risk_score", 0) for l in loans) / total_loans, 2
        ) if total_loans else 0

        predicted_defaults = sum(
            1 for l in loans if l.get("risk_score", 0) > 70
        )

        total_amount = sum(l.get("amount", 0) for l in loans)

        main = QVBoxLayout(self)

        title = QLabel("LoanOps Copilot – Executive Summary")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("pageTitle")
        main.addWidget(title)

        cards = QHBoxLayout()
        cards.addWidget(self.metric_card("Total Loans", total_loans))
        cards.addWidget(self.metric_card("High Risk Loans", high_risk))
        cards.addWidget(self.metric_card("Avg Risk Score", avg_risk))
        cards.addWidget(self.metric_card("Predicted Defaults (30d)", predicted_defaults))
        main.addLayout(cards)

        exposure = QLabel(
            f"💰 Total Portfolio Exposure: ₹{total_amount:,.0f}"
        )
        exposure.setObjectName("highlightText")
        main.addWidget(exposure)

        insight = QLabel(
            "🧠 Insight:\n"
            f"{high_risk} loans show elevated risk. "
            "Early intervention can significantly reduce potential defaults."
        )
        insight.setWordWrap(True)
        insight.setObjectName("insightBox")
        main.addWidget(insight)

    def metric_card(self, title, value):
        card = QFrame()
        card.setObjectName("metricCard")

        layout = QVBoxLayout(card)

        t = QLabel(title)
        t.setAlignment(Qt.AlignCenter)
        t.setObjectName("cardTitle")

        v = QLabel(str(value))
        v.setAlignment(Qt.AlignCenter)
        v.setObjectName("cardValue")

        layout.addWidget(t)
        layout.addWidget(v)

        return card
