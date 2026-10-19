"""
Generates SAMPLE (synthetic) data for a small cafe, Jul-Sep 2026.
Outputs 4 CSV files into ./data/ : menu, sales, wastage, expenses.
NOTE: This is dummy data. Say so clearly in your README and LinkedIn post.
"""
import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
os.makedirs("data", exist_ok=True)

# ---------- MENU (price and ingredient cost in Rs) ----------
menu = pd.DataFrame(
    [
        ("Filter Coffee", "Beverages", 30, 12),
        ("Masala Chai", "Beverages", 20, 7),
        ("Cold Coffee", "Beverages", 90, 38),
        ("Mojito", "Beverages", 80, 30),
        ("Veg Sandwich", "Snacks", 70, 32),
        ("Cheese Sandwich", "Snacks", 90, 55),
        ("French Fries", "Snacks", 80, 28),
        ("Veg Puff", "Snacks", 25, 14),
        ("Samosa", "Snacks", 15, 6),
        ("Maggi", "Snacks", 50, 20),
        ("Veg Burger", "Meals", 80, 48),
        ("Fried Rice", "Meals", 110, 62),
        ("Brownie", "Desserts", 70, 40),
        ("Ice Cream Sundae", "Desserts", 90, 55),
    ],
    columns=["item", "category", "price", "cost"],
)
menu.to_csv("data/menu.csv", index=False)

# how often each item is ordered (relative popularity)
pop = np.array([14, 14, 8, 5, 8, 6, 7, 6, 10, 7, 5, 4, 4, 4], dtype=float)
pop /= pop.sum()

# busy hours: peaks around 9-10 am and 5-7 pm
hours = np.arange(8, 22)
hour_w = np.array([6, 12, 10, 6, 8, 10, 6, 5, 8, 12, 14, 10, 6, 3], dtype=float)
hour_w /= hour_w.sum()

# ---------- SALES ----------
start = date(2026, 7, 1)
n_days = 92  # Jul 1 to Sep 30
rows = []
order_id = 1

for d in range(n_days):
    day = start + timedelta(days=d)
    weekend = day.weekday() >= 5
    n_orders = max(int(rng.normal(180 if weekend else 120, 15)), 40)
    order_hours = rng.choice(hours, size=n_orders, p=hour_w)

    for h in order_hours:
        minute = int(rng.integers(0, 60))
        n_items = int(rng.choice([1, 2, 3], p=[0.5, 0.35, 0.15]))
        picked = rng.choice(len(menu), size=n_items, replace=False, p=pop)
        discount = 10 if 15 <= h < 17 else 0  # happy-hour offer
        pay = rng.choice(["UPI", "Cash", "Card"], p=[0.6, 0.3, 0.1])

        for i in picked:
            qty = int(rng.choice([1, 2], p=[0.8, 0.2]))
            rows.append(
                {
                    "order_id": order_id,
                    "date": day.isoformat(),
                    "time": f"{h:02d}:{minute:02d}",
                    "item": menu.loc[i, "item"],
                    "category": menu.loc[i, "category"],
                    "qty": qty,
                    "unit_price": int(menu.loc[i, "price"]),
                    "discount_pct": discount,
                    "payment_mode": pay,
                }
            )
        order_id += 1

pd.DataFrame(rows).to_csv("data/sales.csv", index=False)

# ---------- WASTAGE (perishables: avg units wasted per day) ----------
waste_mean = {
    "Veg Puff": 3,
    "Brownie": 2,
    "Veg Sandwich": 2,
    "Ice Cream Sundae": 1.5,
    "Cheese Sandwich": 1,
}
waste_rows = []
for d in range(n_days):
    day = start + timedelta(days=d)
    for item, mean in waste_mean.items():
        units = int(rng.poisson(mean))
        if units:
            cost = int(menu.loc[menu.item == item, "cost"].iloc[0])
            waste_rows.append(
                {
                    "date": day.isoformat(),
                    "item": item,
                    "units_wasted": units,
                    "wastage_cost": units * cost,
                }
            )
pd.DataFrame(waste_rows).to_csv("data/wastage.csv", index=False)

# ---------- MONTHLY EXPENSES (Rs) ----------
expense_rows = []
for month in ["2026-07", "2026-08", "2026-09"]:
    for category, amount in [
        ("Rent", 25000),
        ("Salaries", 40000),
        ("Electricity", 6000),
        ("Gas", 4000),
        ("Miscellaneous", 3000),
    ]:
        expense_rows.append({"month": month, "category": category, "amount": amount})
pd.DataFrame(expense_rows).to_csv("data/expenses.csv", index=False)

print("Done. Files saved in ./data/ (menu, sales, wastage, expenses)")
print(f"Sales rows: {len(rows)} | Orders: {order_id - 1}")