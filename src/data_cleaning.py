"""
Reusable data cleaning functions for the A/B test campaign dataset.
Used by notebooks/01_eda_and_stats.ipynb
"""

import pandas as pd

COLUMN_MAP = {
    'Campaign Name': 'campaign_name',
    'Date': 'date',
    'Spend [USD]': 'spend',
    '# of Impressions': 'impressions',
    'Reach': 'reach',
    '# of Website Clicks': 'clicks',
    '# of Searches': 'searches',
    '# of View Content': 'view_content',
    '# of Add to Cart': 'add_to_cart',
    '# of Purchase': 'purchases'
}

COUNT_COLUMNS = ['impressions', 'reach', 'clicks', 'searches', 'view_content', 'add_to_cart', 'purchases']


def load_campaign_csv(filepath):
    """Load a raw campaign CSV (semicolon-delimited)."""
    return pd.read_csv(filepath, delimiter=';')


def clean_campaign_data(df, drop_na=True):
    """
    Clean a raw campaign dataframe: drop rows with missing data,
    rename columns to snake_case, parse dates, and enforce integer types.
    """
    if drop_na:
        df = df.dropna().reset_index(drop=True)

    df = df.rename(columns=COLUMN_MAP)
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    df[COUNT_COLUMNS] = df[COUNT_COLUMNS].astype(int)

    return df


def load_and_clean(filepath, drop_na=True):
    """Convenience function: load a raw CSV and return it fully cleaned."""
    df = load_campaign_csv(filepath)
    return clean_campaign_data(df, drop_na=drop_na)