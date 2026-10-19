"""
Check each recommendation's numbers, one at a time.
Usage:  python verify.py 1     (then 2, 3, 4, 5)
"""
import sys

import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", None)

sales = pd.read_csv("data/sales.csv", parse_dates=["date"])
menu = pd.read_csv("data/menu.csv")
waste = pd.read_csv("data/wastage.csv")

df = sales.merge(menu[["item", "cost"]], on="item")
df["gross"] = df.qty * df.unit_price
df["revenue"] = df.gross * (1 - df.discount_pct / 100)
df["profit"] = df.revenue - df.qty * df.cost
df["hour"] = df.time.str[:2].astype(int)
df["weekday"] = df.date.dt.day_name()


def rec1():
    print("REC 1: Low-margin bestsellers")
    t = df.groupby("item").agg(units=("qty", "sum"), revenue=("revenue", "sum"),
                               profit=("profit", "sum"))
    t["margin_pct"] = (t.profit / t.revenue * 100).round(1)
    print(t.loc[["Cheese Sandwich", "Veg Sandwich", "Veg Burger", "Ice Cream Sundae"]].round(0))
    units = int(t.loc["Cheese Sandwich", "units"])
    print(f"\nRs 10 price rise on {units} Cheese Sandwiches = Rs {units * 10} extra per quarter")
    print("(assumes sales stay the same; a real price rise may reduce units a little)")


def rec2():
    print("REC 2: The 3-5 pm discount")
    cost_of_discount = (df.gross - df.revenue).sum()
    print(f"Total discount given: Rs {cost_of_discount:.0f}")
    o = df.groupby(df.discount_pct > 0).agg(orders=("order_id", "nunique"),
                                            profit=("profit", "sum"))
    o["profit_per_order"] = (o.profit / o.orders).round(1)
    o.index = ["No discount", "Discount (3-5 pm)"]
    print(o.round(0))
    h = df.groupby("hour").order_id.nunique()
    print("\nOrders at 15h (3 pm):", h[15], "| 16h (4 pm):", h[16])
    print("Slowest hour overall:", h.idxmin(), "h with", h.min(), "orders")


def rec3():
    print("REC 3: Wastage")
    w = waste.groupby("item").wastage_cost.sum().sort_values(ascending=False)
    print(w)
    total = w.sum()
    top2 = w[["Brownie", "Ice Cream Sundae"]].sum()
    print(f"\nTotal wastage: Rs {total} | Brownie + Sundae: Rs {top2} ({top2 / total:.0%})")
    print(f"30% cut on those two saves about Rs {top2 * 0.3:.0f} per quarter")


def rec4():
    print("REC 4: Peak hours")
    h = df.groupby("hour").agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"))
    print(h.sort_values("orders", ascending=False).head(5).round(0))
    peak = h.loc[[9, 10, 17, 18, 19], "revenue"].sum() / h.revenue.sum()
    print(f"\nHours 9-10 am and 5-7 pm bring {peak:.0%} of total revenue")


def rec5():
    print("REC 5: Weekend vs weekday")
    d = df.groupby(["date", "weekday"]).revenue.sum().reset_index()
    d["type"] = d.weekday.isin(["Saturday", "Sunday"]).map({True: "Weekend", False: "Weekday"})
    a = d.groupby("type").revenue.mean()
    print(a.round(0))
    print(f"\nWeekend earns {a['Weekend'] / a['Weekday'] - 1:.0%} more per day")


steps = {"1": rec1, "2": rec2, "3": rec3, "4": rec4, "5": rec5}
choice = sys.argv[1] if len(sys.argv) > 1 else ""
if choice in steps:
    steps[choice]()
else:
    print("Usage: python verify.py 1   (use 1 to 5)")