from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFrame
)
from PyQt5.QtCore import Qt

from modules.origination import Origination
from modules.monitoring import Monitoring
from modules.analytics import Analytics
from modules.executive_summary import ExecutiveSummary


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LoanOps Copilot")
        self.setGeometry(200, 100, 1000, 600)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # ---------- TITLE ----------
        title = QLabel("LoanOps Copilot – Operations Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        subtitle = QLabel(
            "Reimagining loan operations with predictive intelligence"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitle")
        main_layout.addWidget(subtitle)

        # ---------- CARD CONTAINER ----------
        card_container = QHBoxLayout()

        card_container.addWidget(
            self.dashboard_card(
                "📄 Loan Origination",
                "Create and onboard new loans efficiently",
                self.open_origination
            )
        )

        card_container.addWidget(
            self.dashboard_card(
                "📊 Loan Monitoring",
                "Track risk, defaults, and alerts",
                self.open_monitoring
            )
        )

        card_container.addWidget(
            self.dashboard_card(
                "📈 Analytics",
                "Portfolio insights & trends",
                self.open_analytics
            )
        )

        card_container.addWidget(
            self.dashboard_card(
                "🧠 Executive Summary",
                "CXO-ready portfolio overview",
                self.open_executive_summary
            )
        )

        main_layout.addLayout(card_container)

        footer = QLabel(
            "Built for LMA Edge Hackathon • Desktop-first • Commercially viable"
        )
        footer.setAlignment(Qt.AlignCenter)
        footer.setObjectName("footerText")
        main_layout.addWidget(footer)

    # ---------- DASHBOARD CARD ----------
    def dashboard_card(self, title_text, desc_text, action):
        card = QFrame()
        card.setObjectName("dashboardCard")
        card.setFixedWidth(220)

        layout = QVBoxLayout(card)

        title = QLabel(title_text)
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("cardTitle")

        desc = QLabel(desc_text)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setObjectName("cardDesc")

        btn = QPushButton("Open")
        btn.clicked.connect(action)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addStretch()
        layout.addWidget(btn)

        return card

    # ---------- NAVIGATION ----------
    def open_origination(self):
        self.o = Origination()
        self.o.show()

    def open_monitoring(self):
        self.m = Monitoring()
        self.m.show()

    def open_analytics(self):
        self.a = Analytics()
        self.a.show()

    def open_executive_summary(self):
        self.e = ExecutiveSummary()
        self.e.show()
