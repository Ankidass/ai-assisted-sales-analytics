from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
data = pd.read_csv(ROOT / "data" / "sales_data.csv", parse_dates=["OrderDate"])
out = ROOT / "outputs"
out.mkdir(exist_ok=True)

# Validate basic fields and calculate metrics.
required = ["OrderID", "OrderDate", "Product", "Category", "UnitsSold", "RevenueINR", "EstimatedProfitINR"]
missing = data[required].isna().sum()
print("Missing values in required fields:")
print(missing[missing > 0] if (missing > 0).any() else "None")

data["Month"] = data["OrderDate"].dt.to_period("M").astype(str)
category = data.groupby("Category", as_index=False).agg(
    Orders=("OrderID", "count"),
    Units_Sold=("UnitsSold", "sum"),
    Revenue_INR=("RevenueINR", "sum"),
    Estimated_Profit_INR=("EstimatedProfitINR", "sum"),
)
category["Profit_Margin_%"] = (category["Estimated_Profit_INR"] / category["Revenue_INR"] * 100).round(1)
category.to_csv(out / "category_summary.csv", index=False)

monthly = data.groupby("Month", as_index=False).agg(
    Orders=("OrderID", "count"),
    Revenue_INR=("RevenueINR", "sum"),
    Estimated_Profit_INR=("EstimatedProfitINR", "sum"),
)
monthly.to_csv(out / "monthly_summary.csv", index=False)

# Load data into a local SQLite database so the included SQL can be practiced.
db_path = ROOT / "sales_demo.sqlite"
with sqlite3.connect(db_path) as conn:
    data.drop(columns=["Month"], errors="ignore").to_sql("sales_data", conn, if_exists="replace", index=False)
    result = pd.read_sql_query(
        "SELECT Category, ROUND(SUM(RevenueINR),2) AS RevenueINR "
        "FROM sales_data GROUP BY Category ORDER BY RevenueINR DESC", conn
    )
print("\nRevenue by category:")
print(result.to_string(index=False))
print(f"\nSaved outputs to {out} and SQLite database to {db_path}")
