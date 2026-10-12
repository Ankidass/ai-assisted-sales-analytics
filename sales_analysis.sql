-- AI-Assisted Sales Analytics: SQL practice queries
-- Table assumed: sales_data; import data/sales_data.csv first.

-- 1. Overall sales KPIs
SELECT COUNT(*) AS order_count,
       SUM(UnitsSold) AS units_sold,
       ROUND(SUM(RevenueINR), 2) AS total_revenue_inr,
       ROUND(SUM(EstimatedProfitINR), 2) AS estimated_profit_inr
FROM sales_data;

-- 2. Revenue and estimated profit by category
SELECT Category,
       SUM(UnitsSold) AS units_sold,
       ROUND(SUM(RevenueINR), 2) AS revenue_inr,
       ROUND(SUM(EstimatedProfitINR), 2) AS estimated_profit_inr,
       ROUND(100.0 * SUM(EstimatedProfitINR) / NULLIF(SUM(RevenueINR), 0), 1) AS profit_margin_pct
FROM sales_data
GROUP BY Category
ORDER BY revenue_inr DESC;

-- 3. Monthly revenue trend
SELECT SUBSTR(OrderDate, 1, 7) AS month,
       ROUND(SUM(RevenueINR), 2) AS revenue_inr
FROM sales_data
GROUP BY SUBSTR(OrderDate, 1, 7)
ORDER BY month;

-- 4. Products to review: lower revenue than overall product average
WITH product_revenue AS (
  SELECT Product, SUM(RevenueINR) AS revenue_inr
  FROM sales_data
  GROUP BY Product
)
SELECT Product, ROUND(revenue_inr, 2) AS revenue_inr
FROM product_revenue
WHERE revenue_inr < (SELECT AVG(revenue_inr) FROM product_revenue)
ORDER BY revenue_inr;
