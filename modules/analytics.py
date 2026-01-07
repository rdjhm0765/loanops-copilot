# modules/analytics.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from utils.data_handler import load_loans

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Analytics(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Analytics Dashboard")

        layout = QVBoxLayout(self)

        title = QLabel("Portfolio Analytics")
        title.setObjectName("title")
        layout.addWidget(title)

        # Text summary
        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)

        # Chart area
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.refresh_stats()

    def refresh_stats(self):
        loans = load_loans()

        total_loans = len(loans)
        total_amount = sum(l["amount"] for l in loans) if loans else 0

        high = len([l for l in loans if l["risk_label"] == "High"])
        medium = len([l for l in loans if l["risk_label"] == "Medium"])
        low = len([l for l in loans if l["risk_label"] == "Low"])

        self.summary_label.setText(
            f"Total Loans: {total_loans}\n"
            f"Total Amount: ₹{total_amount}\n"
            f"High Risk: {high} | Medium Risk: {medium} | Low Risk: {low}"
        )

        # ---- PIE CHART ----
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        labels = ["High Risk", "Medium Risk", "Low Risk"]
        values = [high, medium, low]

        if sum(values) == 0:
            ax.text(0.5, 0.5, "No loan data available", ha="center", va="center")
        else:
            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90
            )
            ax.set_title("Risk Distribution")

        self.canvas.draw()
