from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
    QListWidgetItem, QPushButton, QLabel, QFrame, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt
from utils.data_handler import load_loans, save_loans
from utils.ml_risk_model import LoanRiskMLModel
import json

class Monitoring(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Monitoring with ML Risk Analytics")
        self.setMinimumSize(1000, 650)
        
        # Initialize ML model
        self.ml_model = LoanRiskMLModel()
        
        self.init_ui()
        self.load_loans()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("🤖 Loan Portfolio - ML Risk Analytics")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)
        
        # Top controls
        controls = QHBoxLayout()
        
        train_btn = QPushButton("🧠 Train ML Model")
        train_btn.setToolTip("Train model on existing loan data")
        train_btn.clicked.connect(self.train_model)
        controls.addWidget(train_btn)
        
        repredict_btn = QPushButton("🔄 Re-predict All Loans")
        repredict_btn.setToolTip("Use trained model to re-assess all loans")
        repredict_btn.clicked.connect(self.repredict_all)
        controls.addWidget(repredict_btn)
        
        controls.addStretch()
        
        # Model status
        self.model_status = QLabel("Model Status: Not Trained")
        self.model_status.setObjectName("subtitle")
        controls.addWidget(self.model_status)
        
        main_layout.addLayout(controls)
        
        # Content area
        content = QHBoxLayout()
        
        # Left: Loan list
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Active Loans:"))
        
        self.list = QListWidget()
        self.list.itemClicked.connect(self.show_loan_details)
        left_panel.addWidget(self.list)
        
        left_frame = QFrame()
        left_frame.setLayout(left_panel)
        content.addWidget(left_frame, 60)
        
        # Right: Details panel
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Loan Details & ML Prediction:"))
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        right_panel.addWidget(self.details_text)
        
        # Feature importance
        self.importance_label = QLabel("Feature Importance will appear after training")
        self.importance_label.setObjectName("subtitle")
        self.importance_label.setWordWrap(True)
        right_panel.addWidget(self.importance_label)
        
        right_frame = QFrame()
        right_frame.setLayout(right_panel)
        content.addWidget(right_frame, 40)
        
        main_layout.addLayout(content)
        
        self.setLayout(main_layout)
        self.update_model_status()

    def load_loans(self):
        """Load and display all loans"""
        self.list.clear()
        loans = load_loans()
        
        for idx, loan in enumerate(loans):
            risk_label = loan.get('risk_label', 'Unknown')
            risk_score = loan.get('risk_score', 0)
            
            item_text = (
                f"{loan['borrower']} | "
                f"₹{loan['amount']} | "
                f"Risk: {risk_label} ({risk_score})"
            )
            
            item = QListWidgetItem(item_text)
            
            # Color code by risk
            if risk_label == "High":
                item.setForeground(Qt.red)
            elif risk_label == "Medium":
                item.setForeground(Qt.darkYellow)
            else:
                item.setForeground(Qt.darkGreen)
            
            # Store loan data in item
            item.setData(Qt.UserRole, idx)
            self.list.addItem(item)

    def show_loan_details(self, item):
        """Show detailed info for selected loan"""
        loans = load_loans()
        idx = item.data(Qt.UserRole)
        loan = loans[idx]
        
        # Format details
        details = f"""
=== BORROWER INFORMATION ===
Name: {loan['borrower']}
Loan Amount: ₹{loan['amount']}
PAN: {loan.get('pan', 'Not provided')}
Annual Income: ₹{loan.get('annual_income', 'Not provided')}

=== RISK ASSESSMENT ===
Risk Label: {loan['risk_label']}
Risk Score: {loan['risk_score']}/100
ML Confidence: {loan.get('ml_confidence', 'N/A')}

=== PREDICTION METHOD ===
{loan.get('prediction_method', 'Rule-based (default)')}
        """
        
        self.details_text.setText(details.strip())

    def train_model(self):
        """Train ML model on existing loans"""
        loans = load_loans()
        
        if len(loans) < 5:
            QMessageBox.warning(
                self,
                "Insufficient Data",
                f"Need at least 5 loans to train model. Currently have {len(loans)} loans.\n\n"
                "Add more loans through Loan Origination first."
            )
            return
        
        # Train model
        success = self.ml_model.train(loans)
        
        if success:
            QMessageBox.information(
                self,
                "Training Complete",
                f"ML model trained successfully on {len(loans)} loans!\n\n"
                "You can now use 'Re-predict All Loans' to apply the model."
            )
            self.update_model_status()
            self.show_feature_importance()
        else:
            QMessageBox.warning(self, "Training Failed", "Could not train model")

    def repredict_all(self):
        """Re-predict risk for all loans using ML model"""
        if not self.ml_model.is_trained:
            QMessageBox.warning(
                self,
                "Model Not Trained",
                "Please train the ML model first using 'Train ML Model' button"
            )
            return
        
        loans = load_loans()
        updated_count = 0
        
        for loan in loans:
            # Get ML prediction
            risk_score, risk_label, confidence = self.ml_model.predict(loan)
            
            # Update loan data
            loan['risk_score'] = risk_score
            loan['risk_label'] = risk_label
            loan['ml_confidence'] = f"{confidence:.2%}"
            loan['prediction_method'] = 'ML Model (Random Forest)'
            updated_count += 1
        
        # Save updated loans
        save_loans(loans)
        
        # Refresh display
        self.load_loans()
        
        QMessageBox.information(
            self,
            "Re-prediction Complete",
            f"Successfully re-assessed {updated_count} loans using ML model!\n\n"
            "Risk scores and labels have been updated."
        )

    def update_model_status(self):
        """Update model status label"""
        if self.ml_model.is_trained:
            self.model_status.setText("✅ Model Status: Trained & Ready")
            self.model_status.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.model_status.setText("❌ Model Status: Not Trained")
            self.model_status.setStyleSheet("color: red;")

    def show_feature_importance(self):
        """Display which features matter most"""
        importance = self.ml_model.get_feature_importance()
        
        if importance:
            text = "📊 Feature Importance (what drives risk):\n"
            for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
                text += f"\n• {feature}: {score:.2%}"
            
            self.importance_label.setText(text)
            self.importance_label.setStyleSheet("color: #1f3c88; font-weight: 500;")
        else:
            self.importance_label.setText("Train model to see feature importance")