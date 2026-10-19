"""
Step 2: Clean, explore and answer the business questions.
Run from the same folder as generate_cafe_data.py:  python step2_explore.py
Saves summary tables to ./output/ (we'll use these for the dashboard).
"""
import os

import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", None)
os.makedirs("output", exist_ok=True)

# ---------- LOAD ----------
sales = pd.read_csv("data/sales.csv", parse_dates=["date"])
menu = pd.read_csv("data/menu.csv")
waste = pd.read_csv("data/wastage.csv", parse_dates=["date"])
exp = pd.read_csv("data/expenses.csv")

# ---------- QUICK DATA CHECKS ----------
print("=== DATA CHECKS ===")
print("Rows:", len(sales), "| Missing values:", int(sales.isna().sum().sum()),
      "| Duplicate rows:", int(sales.duplicated().sum()))
print("Date range:", sales.date.min().date(), "to", sales.date.max().date())

# ---------- FEATURES ----------
df = sales.merge(menu[["item", "cost"]], on="item", how="left")
df["revenue"] = df.qty * df.unit_price * (1 - df.discount_pct / 100)
df["cogs"] = df.qty * df.cost
df["profit"] = df.revenue - df.cogs
df["hour"] = df.time.str[:2].astype(int)
df["month"] = df.date.dt.strftime("%Y-%m")
df["weekday"] = df.date.dt.day_name()

print("\nTotal revenue: Rs", round(df.revenue.sum()))
print("Gross profit (revenue - ingredient cost): Rs", round(df.profit.sum()))

# ---------- Q1: WHICH ITEMS MAKE / LOSE MONEY? ----------
items = df.groupby("item").agg(units=("qty", "sum"), revenue=("revenue", "sum"),
                               profit=("profit", "sum"))
items["margin_pct"] = (items.profit / items.revenue * 100).round(1)
items = items.sort_values("profit", ascending=False).round(0)
print("\n=== Q1: ITEM PERFORMANCE (sorted by profit) ===")
print(items)
items.to_csv("output/item_performance.csv")

# ---------- Q2: CATEGORY VIEW ----------
cats = df.groupby("category").agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
cats["margin_pct"] = (cats.profit / cats.revenue * 100).round(1)
print("\n=== Q2: CATEGORY PERFORMANCE ===")
print(cats.round(0))
cats.to_csv("output/category_performance.csv")

# ---------- Q3: PEAK HOURS ----------
hours = df.groupby("hour").agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"))
print("\n=== Q3: ORDERS AND REVENUE BY HOUR ===")
print(hours.round(0))
hours.to_csv("output/hourly.csv")

# ---------- Q4: WEEKDAY VS WEEKEND ----------
daily = df.groupby(["date", "weekday"]).revenue.sum().reset_index()
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
wd = daily.groupby("weekday").revenue.mean().reindex(order).round(0)
print("\n=== Q4: AVERAGE DAILY REVENUE BY WEEKDAY ===")
print(wd)
wd.to_csv("output/weekday.csv")

# ---------- Q5: DOES THE DISCOUNT HELP? ----------
disc = df.groupby("discount_pct").agg(orders=("order_id", "nunique"),
                                      revenue=("revenue", "sum"), profit=("profit", "sum"))
disc["profit_per_order"] = (disc.profit / disc.orders).round(1)
print("\n=== Q5: DISCOUNT IMPACT (0 = no discount, 10 = happy hour 3-5 pm) ===")
print(disc.round(0))
disc.to_csv("output/discount_impact.csv")

# ---------- Q6: WASTAGE ----------
w = waste.groupby("item").agg(units_wasted=("units_wasted", "sum"),
                              wastage_cost=("wastage_cost", "sum")).sort_values(
    "wastage_cost", ascending=False)
print("\n=== Q6: WASTAGE BY ITEM ===")
print(w)
w.to_csv("output/wastage_by_item.csv")

# ---------- Q7: MONTHLY P&L ----------
waste["month"] = waste.date.dt.strftime("%Y-%m")
pl = df.groupby("month").agg(revenue=("revenue", "sum"), ingredient_cost=("cogs", "sum"))
pl["wastage"] = waste.groupby("month").wastage_cost.sum()
pl["fixed_expenses"] = exp.groupby("month").amount.sum()
pl["net_profit"] = pl.revenue - pl.ingredient_cost - pl.wastage - pl.fixed_expenses
print("\n=== Q7: MONTHLY PROFIT AND LOSS ===")
print(pl.round(0))
pl.to_csv("output/monthly_pl.csv")

print("\nDone. Tables saved in ./output/")