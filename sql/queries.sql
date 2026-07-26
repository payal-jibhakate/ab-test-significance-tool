-- ============================================
-- A/B Test Significance Tool
-- Database: ab_test_analysis
-- ============================================

-- Schema

CREATE DATABASE IF NOT EXISTS ab_test_analysis;
USE ab_test_analysis;

CREATE TABLE campaign_performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_name VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    spend INT NOT NULL,
    impressions INT NOT NULL,
    reach INT NOT NULL,
    clicks INT NOT NULL,
    searches INT NOT NULL,
    view_content INT NOT NULL,
    add_to_cart INT NOT NULL,
    purchases INT NOT NULL
);

SELECT COUNT(*) FROM campaign_performance;
SELECT campaign_name, COUNT(*) FROM campaign_performance GROUP BY campaign_name;

-- Query 1 — Overall performance comparison
-- Answers: Which campaign performed better overall, and which was more cost-efficient?
SELECT 
    campaign_name,
    SUM(spend) AS total_spend,
    SUM(purchases) AS total_purchases,
    ROUND(AVG(purchases), 2) AS avg_daily_purchases,
    ROUND(SUM(spend) / SUM(purchases), 2) AS cost_per_purchase
FROM campaign_performance
GROUP BY campaign_name;


-- Query 2 — Funnel conversion rates in SQL
-- Answers: Where does each campaign lose the most users in the funnel (impressions -> clicks -> cart -> purchase)?
SELECT
    campaign_name,
    ROUND(SUM(clicks) / SUM(impressions), 4) AS click_through_rate,
    ROUND(SUM(add_to_cart) / SUM(clicks), 4) AS cart_rate,
    ROUND(SUM(purchases) / SUM(add_to_cart), 4) AS purchase_rate
FROM campaign_performance
GROUP BY campaign_name;

-- Query 3 — Best and worst single day per campaign
-- Answers: What was each campaign's strongest and weakest day, and were both campaigns affected by the same external event?
SELECT campaign_name, date, purchases
FROM (
    SELECT 
        campaign_name, 
        date, 
        purchases,
        RANK() OVER (PARTITION BY campaign_name ORDER BY purchases DESC) AS rank_high,
        RANK() OVER (PARTITION BY campaign_name ORDER BY purchases ASC) AS rank_low
    FROM campaign_performance
) ranked
WHERE rank_high = 1 OR rank_low = 1
ORDER BY campaign_name, purchases DESC;


-- Query 4 — Day-of-week pattern
-- Answers: Is there a weekday/weekend pattern in purchase performance for either campaign?
SELECT
    campaign_name,
    DAYNAME(date) AS day_of_week,
    ROUND(AVG(purchases), 1) AS avg_purchases
FROM campaign_performance
GROUP BY campaign_name, DAYNAME(date)
ORDER BY campaign_name, AVG(purchases) DESC;

-- Query 5 — Flag high cost-per-purchase days
-- Answers: Which specific days were unusually inefficient (>1.5x that campaign's own average cost-per-purchase), worth investigating?
SELECT
    campaign_name,
    date,
    spend,
    purchases,
    ROUND(spend / purchases, 2) AS cost_per_purchase
FROM campaign_performance
WHERE (spend / purchases) > (
    SELECT AVG(spend / purchases) * 1.5
    FROM campaign_performance AS cp2
    WHERE cp2.campaign_name = campaign_performance.campaign_name
)
ORDER BY cost_per_purchase DESC;