from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from utils.data_handler import load_loans

class Monitoring(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Monitoring")

        layout = QVBoxLayout()
        self.list = QListWidget()
        layout.addWidget(self.list)
        self.setLayout(layout)

        self.load_loans()

    def load_loans(self):
        self.list.clear()
        for loan in load_loans():
            item = QListWidgetItem(
                f"{loan['borrower']} | ₹{loan['amount']} | Risk: {loan['risk_label']}"
            )
            if loan["risk_label"] == "High":
                item.setForeground(Qt.red)
            self.list.addItem(item)
