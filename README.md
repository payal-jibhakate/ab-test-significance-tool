\# A/B Test Statistical Significance Tool



A reusable Streamlit tool that determines whether A/B test results are statistically significant — built on a real e-commerce ad campaign dataset (Facebook Ads vs AdWords, August 2019).



\## The Problem

Businesses run A/B tests constantly, but many teams eyeball the results and declare a "winner" without checking whether the difference is statistically real or just random noise. This project analyzes a real Control vs Test ad campaign, and builds a tool that automates the correct statistical workflow for any future test.



\## Key Finding

Despite the Test campaign having a \~2x higher click-through rate, there was \*\*no statistically significant difference in purchases\*\* between the two campaigns (Mann-Whitney U, p = 0.958, Cohen's d = 0.008). Control achieved the same results at a lower cost per purchase. Full analysis in \[`reports/business\_insights.md`](reports/business\_insights.md).



\## The Tool

Unlike a one-off analysis, the Streamlit app in `app/streamlit\_app.py` accepts \*\*any\*\* A/B test CSV — not just this dataset. It automatically:

\- Detects the correct statistical test to use (t-test vs. Mann-Whitney U) based on a live normality check

\- Calculates significance and effect size

\- Returns a plain-English verdict, not just a raw p-value



\## Tech Stack

Python (Pandas, SciPy, Matplotlib) · MySQL · Streamlit



\## Project Structure

data/ raw and cleaned datasets

notebooks/ EDA and statistical analysis walkthrough

sql/ database schema and business queries

app/ the Streamlit significance-testing tool

reports/ executive business insights summary



\## Dataset

Real Kaggle dataset: \[Facebook Ads vs AdWords Campaign](https://www.kaggle.com/datasets/amirmotefaker/ab-testing-dataset), simulating daily performance of two ad campaigns over August 2019.



\## How to Run

pip install -r requirements.txt

streamlit run app/streamlit\_app.py



\## Author

Payal Jibhakate — \[GitHub](https://github.com/payal-jibhakate)

\[LinkedIn](https://linkedin.com/in/payal-jibhakate)





