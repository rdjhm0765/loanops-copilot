import json
import os

DATA_FILE = "data/sample_loans.json"

def load_loans():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_loans(loans):
    with open(DATA_FILE, "w") as f:
        json.dump(loans, f, indent=4)
