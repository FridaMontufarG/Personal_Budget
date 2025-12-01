import pandas as pd
import numpy as np
from datetime import datetime
import random

# Seed for reproducibility
random.seed(42)
np.random.seed(42)

fixed_salary = 1600

# Percentages based on fixed salary
category_percentages = {
    'Food': 0.14,       # Need  → 224
    'Housing': 0.28,    # Need  → 448
    'Transport': 0.08,  # Need  → 128
    'Leisure': 0.18,    # Want  → 288
    'Others': 0.12      # Want  → 192
}

category_priority = {
    'Food': 'Need',
    'Housing': 'Need',
    'Transport': 'Need',
    'Leisure': 'Want',
    'Others': 'Want'
}

# Create Budgets
base_budgets = {cat: fixed_salary * pct for cat, pct in category_percentages.items()}

rows = []
pay_methods = ['Card', 'Cash', 'Transfer']

for month in range(1, 13):
    dates = pd.date_range(datetime(2025, month, 1), periods=28)

    # Slightly variable income (tendency > expenses)
    variable_income = round(np.random.normal(90, 70), 2)

    total_income = fixed_salary + variable_income

    rows.append([
        datetime(2025, month, 1),
        "Income",
        "Income",
        "Salary + Extras",
        total_income,
        "",
        "Income"
    ])

    # Seasonal spending patterns
    seasonal_factor = {
        1: 1.06, 3: 1.09, 6: 1.10,
        7: 1.13, 8: 1.10, 11: 1.12, 12: 1.18
    }.get(month, 1)

    for cat, base_budget in base_budgets.items():

        # Monthly adjusted budget (budget respects salary percentage!)
        month_budget = base_budget * seasonal_factor * np.random.uniform(0.84, 1.12)

        # Distribution of transactions
        n_tx = random.randint(5, 10) if cat == 'Food' else random.randint(3, 6)
        tx_mean = month_budget / n_tx
        tx_amounts = np.abs(np.random.normal(tx_mean, tx_mean * 0.22, n_tx))
        tx_amounts *= month_budget / tx_amounts.sum()

        for amt in tx_amounts:

            desc = cat + " expense"
            if cat == 'Food' and random.random() < 0.25:
                desc = random.choice(["Groceries", "Restaurant", "Snacks", "Coffee"])
            if cat == 'Leisure' and random.random() < 0.30:
                desc = random.choice(["Cinema", "Games", "Bar", "Concert"])
            if cat == 'Others' and random.random() < 0.20:
                desc = random.choice(["Clothes", "Gifts", "Phone"])

            rows.append([
                random.choice(dates),
                cat,
                "Expense",
                desc,
                round(amt, 2),
                category_priority[cat],
                "Expense"
            ])

df = pd.DataFrame(rows, columns=['Date','Category','Type','Description','Amount','Priority'])
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

# Add additional info
df.insert(0, 'ID', range(1, len(df) + 1))
df['PaymentMethod'] = [random.choice(pay_methods) for _ in df.index]
df['Week'] = df['Date'].dt.isocalendar().week
df['Month'] = df['Date'].dt.to_period('M').astype(str)

# Limit to 500 rows
df = df.head(500)

filename = "Transactions.xlsx"
with pd.ExcelWriter(filename) as writer:
    df.to_excel(writer, sheet_name='Transactions', index=False)



