import pytesseract
from PIL import Image
import pdfplumber
import re
import json

class DocumentParser:
    def __init__(self):
        # Common field patterns in loan documents
        self.patterns = {
            'borrower_name': [
                r'(?:applicant|borrower|name)[\s:]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'name[\s:]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'
            ],
            'loan_amount': [
                r'(?:loan amount|amount)[\s:]+₹?\s*(\d+(?:,\d+)*)',
                r'(?:loan amount|amount)[\s:]+(?:Rs\.?|INR)?\s*(\d+(?:,\d+)*)'
            ],
            'pan': [
                r'PAN[\s:]+([A-Z]{5}\d{4}[A-Z])',
                r'(?:PAN|pan)[\s:]*([A-Z]{5}\d{4}[A-Z])'
            ],
            'annual_income': [
                r'(?:annual income|yearly income)[\s:]+₹?\s*(\d+(?:,\d+)*)',
            ],
            'credit_score': [
                r'(?:credit score|CIBIL)[\s:]+(\d{3})',
            ]
        }
    
    def extract_from_image(self, image_path):
        """Extract text from image file using OCR"""
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return self.parse_text(text)
        except Exception as e:
            return {"error": f"Image parsing failed: {str(e)}"}
    
    def extract_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return self.parse_text(text)
        except Exception as e:
            return {"error": f"PDF parsing failed: {str(e)}"}
    
    def parse_text(self, text):
        """Extract loan details from text using patterns"""
        extracted_data = {}
        
        for field, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    # Clean amount values (remove commas)
                    if 'amount' in field or 'income' in field:
                        value = value.replace(',', '')
                    extracted_data[field] = value
                    break
        
        return extracted_data
    
    def validate_extraction(self, data):
        """Check if required fields are present"""
        required = ['borrower_name', 'loan_amount']
        missing = [field for field in required if field not in data]
        
        return {
            'is_valid': len(missing) == 0,
            'missing_fields': missing,
            'extracted_data': data
        }