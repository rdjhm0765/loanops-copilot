# utils/datahandler.py

from utils.db import get_collection

loans_col = get_collection("loans")

def load_loans():
    return list(loans_col.find({}, {"_id": 0}))

def save_loan(loan):
    loans_col.insert_one(loan)

def update_loan(loan_id, updates):
    loans_col.update_one(
        {"loan_id": loan_id},
        {"$set": updates}
    )

def delete_loan(loan_id):
    loans_col.delete_one({"loan_id": loan_id})
