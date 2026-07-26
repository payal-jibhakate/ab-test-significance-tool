# 📊 A/B Test Statistical Significance Tool

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

A reusable Streamlit tool that determines whether A/B test results are statistically significant — built on a real e-commerce ad campaign dataset (Facebook Ads vs AdWords, August 2019).

---

## 🎯 The Problem

Businesses run A/B tests constantly, but many teams eyeball the results and declare a "winner" without checking whether the difference is statistically real or just random noise. This project analyzes a real Control vs Test ad campaign, and builds a tool that automates the correct statistical workflow for any future test.

---

## 🔑 Key Finding

Despite the Test campaign having a **~2x higher click-through rate**, there was **no statistically significant difference in purchases** between the two campaigns.

| Metric | Result |
|---|---|
| Test Used | Mann-Whitney U |
| p-value | 0.958 |
| Effect Size (Cohen's d) | 0.008 (negligible) |
| Cost per Purchase | Control $4.41 vs Test $4.92 |

Control achieved the same results at a lower cost. Full analysis in [`reports/business_insights.md`](reports/business_insights.md).

---

## 🛠️ The Tool

Unlike a one-off analysis, the Streamlit app in `app/streamlit_app.py` accepts **any** A/B test CSV — not just this dataset. It automatically:

- ✅ Detects the correct statistical test to use (t-test vs. Mann-Whitney U) based on a live normality check
- ✅ Calculates significance and effect size
- ✅ Returns a plain-English verdict, not just a raw p-value

---

## 📁 Project Structure

| Folder | Contents |
|---|---|
| `data/` | Raw and cleaned datasets |
| `notebooks/` | EDA and statistical analysis walkthrough |
| `sql/` | Database schema and business queries |
| `app/` | The Streamlit significance-testing tool |
| `reports/` | Executive business insights summary |

---

## 📦 Dataset Source

| Field | Details |
|---|---|
| Name | Facebook Ads vs AdWords Campaign |
| Source | [Kaggle](https://www.kaggle.com/datasets/amirmotefaker/ab-testing-dataset) |
| Columns | Spend, Impressions, Reach, Clicks, Searches, Add to Cart, Purchases |
| Time Period | August 2019 |

---

## ▶️ How to Run
pip install -r requirements.txt
streamlit run app/streamlit_app.py

---

## 👤 Author

**Payal Jibhakate** — Aspiring Data Analyst | Python | SQL | Power BI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/payal-jibhakate)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/payal-jibhakate)

---

⭐ If you found this project helpful, please give it a star!