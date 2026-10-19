# Cafe Sales & Profit Analysis

An end-to-end data analytics project that answers one question for a small cafe owner: **where is the cafe making and losing money?**

> **Note:** This project uses **synthetic sample data** that I generated with Python to simulate a small cafe (Jul-Sep 2026). It is not a real client's data.

## Dashboard

![Dashboard](dashboard.png)

Full PDF: [`cafe_dashboard.pdf`](cafe_dashboard.pdf) | Insights report: [`insights_report.pdf`](insights_report.pdf)

## What I analysed

- Which items earn the most profit, and which have thin margins
- Peak hours and weekday vs weekend sales
- Whether the 3-5 pm happy-hour discount actually helps
- How much wastage costs and where it comes from
- Monthly profit and loss after ingredient cost, wastage and fixed expenses

## Key findings

- Revenue of about 13.46 lakh and gross profit of about 6.98 lakh over 3 months; net profit about 4.34 lakh
- Cheese Sandwich, Veg Burger and Ice Cream Sundae have margins of only 38-39%, versus 60-65% for chai, fries and filter coffee
- The 10% happy hour reduced profit per order from Rs 57 to Rs 47
- Brownie and Ice Cream Sundae account for 52% of the Rs 30,250 wastage
- 9-10 am and 5-7 pm bring 51% of revenue; weekends earn 43% more per day than weekdays

## Recommendations

1. Raise the Cheese Sandwich price by Rs 10 or trim filling cost (about Rs 14,900 extra profit per quarter)
2. Replace the blanket discount with a high-margin combo (e.g. Masala Chai + Samosa)
3. Make Sundaes to order and bake Brownies in smaller batches (about Rs 4,700 saved per quarter)
4. Plan prep and staff around the two daily peaks
5. Stock up and add staff for weekends

See the full report for details and assumptions.

## Tools

Python (Pandas, NumPy), Power BI, CSV

## Project structure

```
generate_cafe_data.py   # creates the synthetic dataset
step2_explore.py        # cleaning checks + 7 business questions
verify.py               # verifies each recommendation's numbers
data/                   # menu, sales, wastage, expenses (CSV)
output/                 # summary tables used in the dashboard
cafe_dashboard.pbix     # Power BI file
```

## How to run

```bash
pip install pandas numpy
python generate_cafe_data.py
python step2_explore.py
python verify.py 1      # use 1 to 5
```

## Author

Aditi Panigrahi, B.Tech CSE (AI/ML), GITAM, Visakhapatnam
LinkedIn: add your link here | Open to freelance data analytics work for small cafes and food businesses
