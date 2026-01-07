import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

class LoanRiskMLModel:
    """
    Machine Learning model for loan risk prediction.
    Uses Random Forest to classify loans into Low/Medium/High risk.
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = "data/risk_model.pkl"
        self.scaler_path = "data/scaler.pkl"
        
        # Load existing model if available
        self.load_model()
    
    def prepare_features(self, loan_data):
        """
        Convert loan data into features for ML model.
        
        Features:
        - loan_amount: Amount of loan
        - income_ratio: loan_amount / annual_income (if available)
        - has_pan: Whether PAN is provided (1/0)
        """
        features = []
        
        loan_amount = float(loan_data.get('amount', 0))
        annual_income = float(loan_data.get('annual_income', 0)) if loan_data.get('annual_income') else None
        has_pan = 1 if loan_data.get('pan') else 0
        
        # Feature 1: Loan amount (in lakhs for better scaling)
        features.append(loan_amount / 100000)
        
        # Feature 2: Income ratio (loan to income)
        if annual_income and annual_income > 0:
            income_ratio = loan_amount / annual_income
        else:
            income_ratio = 5.0  # Default high ratio if income unknown
        features.append(income_ratio)
        
        # Feature 3: Has PAN documentation
        features.append(has_pan)
        
        return np.array(features).reshape(1, -1)
    
    def train(self, loans_data):
        """
        Train the model on existing loan data.
        Uses existing risk_labels as ground truth.
        """
        if len(loans_data) < 5:
            print("Not enough data to train. Need at least 5 loans.")
            return False
        
        X = []
        y = []
        
        # Prepare training data
        for loan in loans_data:
            features = self.prepare_features(loan)
            X.append(features[0])
            
            # Convert risk_label to numeric (0=Low, 1=Medium, 2=High)
            label = loan.get('risk_label', 'Medium')
            if label == 'Low':
                y.append(0)
            elif label == 'Medium':
                y.append(1)
            else:
                y.append(2)
        
        X = np.array(X)
        y = np.array(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Save model
        self.save_model()
        
        print(f"Model trained on {len(loans_data)} loans")
        return True
    
    def predict(self, loan_data):
        """
        Predict risk for a new loan.
        Returns: (risk_score, risk_label, confidence)
        """
        if not self.is_trained:
            # Fallback to rule-based if model not trained
            return self._rule_based_prediction(loan_data)
        
        # Prepare features
        features = self.prepare_features(loan_data)
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Convert to label
        labels = ['Low', 'Medium', 'High']
        risk_label = labels[prediction]
        
        # Risk score (0-100 scale)
        risk_score = int((prediction * 33) + (probabilities[prediction] * 33))
        risk_score = min(100, max(0, risk_score))
        
        # Confidence
        confidence = float(probabilities[prediction])
        
        return risk_score, risk_label, confidence
    
    def _rule_based_prediction(self, loan_data):
        """
        Fallback rule-based prediction when ML model not trained.
        """
        loan_amount = float(loan_data.get('amount', 0))
        
        # Simple rules
        if loan_amount > 500000:
            return 75, 'High', 0.7
        elif loan_amount > 200000:
            return 50, 'Medium', 0.7
        else:
            return 25, 'Low', 0.7
    
    def save_model(self):
        """Save trained model to disk"""
        try:
            os.makedirs('data', exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            print("Model saved successfully")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def load_model(self):
        """Load trained model from disk"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.is_trained = True
                print("Model loaded successfully")
            else:
                print("No saved model found. Will use rule-based prediction.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.is_trained = False
    
    def retrain_on_new_data(self, loans_data):
        """
        Retrain model when new loans are added.
        Should be called periodically as more data comes in.
        """
        return self.train(loans_data)
    
    def get_feature_importance(self):
        """
        Get which features matter most for predictions.
        Useful for explaining decisions.
        """
        if not self.is_trained:
            return None
        
        feature_names = ['Loan Amount (Lakhs)', 'Income Ratio', 'Has PAN']
        importances = self.model.feature_importances_
        
        return {name: float(imp) for name, imp in zip(feature_names, importances)}