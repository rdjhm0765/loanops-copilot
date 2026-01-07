from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QFileDialog, QHBoxLayout, QTextEdit
)
from PyQt5.QtCore import Qt
from utils.data_handler import load_loans, save_loans
from utils.ai_model import risk_score, risk_label
from utils.ocr_parser import DocumentParser

class Origination(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Origination")
        self.setMinimumWidth(600)
        
        self.parser = DocumentParser()
        self.extracted_data = {}
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("New Loan Application")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # Document upload section
        upload_section = QHBoxLayout()
        upload_label = QLabel("Upload Loan Document (PDF/Image):")
        self.upload_btn = QPushButton("Choose File")
        self.upload_btn.clicked.connect(self.upload_document)
        upload_section.addWidget(upload_label)
        upload_section.addWidget(self.upload_btn)
        upload_section.addStretch()
        layout.addLayout(upload_section)
        
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("subtitle")
        layout.addWidget(self.file_label)
        
        # Parse button
        parse_btn = QPushButton("Extract Details from Document")
        parse_btn.clicked.connect(self.parse_document)
        layout.addWidget(parse_btn)
        
        # Extracted data display
        layout.addWidget(QLabel("Extracted Information:"))
        self.extracted_text = QTextEdit()
        self.extracted_text.setReadOnly(True)
        self.extracted_text.setMaximumHeight(100)
        layout.addWidget(self.extracted_text)
        
        # Manual entry fields
        layout.addWidget(QLabel("Borrower Name"))
        self.name = QLineEdit()
        layout.addWidget(self.name)

        layout.addWidget(QLabel("Loan Amount (₹)"))
        self.amount = QLineEdit()
        layout.addWidget(self.amount)
        
        layout.addWidget(QLabel("PAN (optional)"))
        self.pan = QLineEdit()
        layout.addWidget(self.pan)
        
        layout.addWidget(QLabel("Annual Income (₹, optional)"))
        self.income = QLineEdit()
        layout.addWidget(self.income)

        # Submit button
        btn = QPushButton("Submit Loan for Risk Assessment")
        btn.clicked.connect(self.submit)
        layout.addWidget(btn)

        self.setLayout(layout)
    
    def upload_document(self):
        """Handle file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Loan Document",
            "",
            "Documents (*.pdf *.png *.jpg *.jpeg);;All Files (*)"
        )
        
        if file_path:
            self.current_file = file_path
            self.file_label.setText(f"Selected: {file_path.split('/')[-1]}")
    
    def parse_document(self):
        """Parse uploaded document"""
        if not hasattr(self, 'current_file'):
            QMessageBox.warning(self, "No File", "Please upload a document first")
            return
        
        try:
            # Determine file type and parse
            if self.current_file.lower().endswith('.pdf'):
                result = self.parser.extract_from_pdf(self.current_file)
            else:
                result = self.parser.extract_from_image(self.current_file)
            
            if 'error' in result:
                QMessageBox.critical(self, "Parsing Error", result['error'])
                return
            
            # Validate extraction
            validation = self.parser.validate_extraction(result)
            self.extracted_data = validation['extracted_data']
            
            # Display extracted data
            display_text = "Extracted Fields:\n"
            for key, value in self.extracted_data.items():
                display_text += f"• {key.replace('_', ' ').title()}: {value}\n"
            
            if validation['missing_fields']:
                display_text += f"\n⚠️ Missing: {', '.join(validation['missing_fields'])}"
            
            self.extracted_text.setText(display_text)
            
            # Auto-fill form fields
            if 'borrower_name' in self.extracted_data:
                self.name.setText(self.extracted_data['borrower_name'])
            if 'loan_amount' in self.extracted_data:
                self.amount.setText(self.extracted_data['loan_amount'])
            if 'pan' in self.extracted_data:
                self.pan.setText(self.extracted_data['pan'])
            if 'annual_income' in self.extracted_data:
                self.income.setText(self.extracted_data['annual_income'])
            
            QMessageBox.information(
                self,
                "Success",
                f"Extracted {len(self.extracted_data)} fields. Please verify and submit."
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Parsing failed: {str(e)}")

    def submit(self):
        """Submit loan application"""
        borrower_name = self.name.text().strip()
        loan_amount = self.amount.text().strip()
        
        if not borrower_name or not loan_amount:
            QMessageBox.warning(self, "Missing Data", "Name and Amount are required")
            return
        
        try:
            # Calculate risk
            score = risk_score(loan_amount)
            label = risk_label(score)

            # Save loan
            loans = load_loans()
            loans.append({
                "borrower": borrower_name,
                "amount": loan_amount,
                "pan": self.pan.text(),
                "annual_income": self.income.text(),
                "risk_score": score,
                "risk_label": label
            })
            save_loans(loans)

            QMessageBox.information(
                self,
                "AI Risk Assessment Complete",
                f"Borrower: {borrower_name}\n"
                f"Amount: ₹{loan_amount}\n"
                f"Risk Level: {label}\n"
                f"Risk Score: {score}"
            )
            
            # Clear form
            self.name.clear()
            self.amount.clear()
            self.pan.clear()
            self.income.clear()
            self.extracted_text.clear()
            self.file_label.setText("No file selected")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Submission failed: {str(e)}")