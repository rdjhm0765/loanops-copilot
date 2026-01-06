from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.data_handler import load_loans

class Analytics(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfolio Analytics")
        self.setGeometry(300, 150, 800, 500)

        layout = QVBoxLayout()

        title = QLabel("Loan Portfolio Risk Analytics")
        title.setObjectName("title")
        layout.addWidget(title)

        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.plot()

    def plot(self):
        loans = load_loans()
        low = sum(1 for l in loans if l["risk_label"] == "Low")
        med = sum(1 for l in loans if l["risk_label"] == "Medium")
        high = sum(1 for l in loans if l["risk_label"] == "High")

        ax = self.canvas.figure.subplots()
        ax.clear()
        ax.bar(["Low", "Medium", "High"], [low, med, high])
        ax.set_title("Risk Distribution Across Portfolio")
        ax.set_ylabel("Number of Loans")
        self.canvas.draw()
