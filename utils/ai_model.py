import random

def risk_score(loan_amount):
    base = random.randint(20, 60)

    if int(loan_amount) > 500000:
        base += 25
    elif int(loan_amount) > 200000:
        base += 15

    return min(base, 100)


def risk_label(score):
    if score <= 35:
        return "Low"
    elif score <= 65:
        return "Medium"
    else:
        return "High"
