import streamlit as st
import pandas as pd
from scipy import stats
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="A/B Test Significance Tool", layout="centered")

st.title("A/B Test Statistical Significance Tool")
st.write("Upload your A/B test data to check if the difference between groups is statistically significant.")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of your data:")
    st.dataframe(df.head())

    st.subheader("Configure Your Test")

    group_col = st.selectbox("Which column identifies the groups (e.g. Control/Test)?", df.columns)
    metric_col = st.selectbox("Which column is the metric you want to compare (e.g. purchases)?", df.columns)

    groups = df[group_col].unique()

    if len(groups) != 2:
        st.warning(f"This tool currently supports exactly 2 groups. Found {len(groups)}: {list(groups)}")
    else:
        group_a_name, group_b_name = groups[0], groups[1]
        group_a = df[df[group_col] == group_a_name][metric_col]
        group_b = df[df[group_col] == group_b_name][metric_col]

        st.success(f"Comparing **{group_a_name}** vs **{group_b_name}** on **{metric_col}**")

        if st.button("Run Significance Test"):

            # Step 1: Check normality
            shapiro_a = stats.shapiro(group_a)
            shapiro_b = stats.shapiro(group_b)
            both_normal = shapiro_a.pvalue > 0.05 and shapiro_b.pvalue > 0.05

            # Step 2: Pick the right test based on normality
            if both_normal:
                test_name = "Independent T-Test"
                stat, p_value = stats.ttest_ind(group_a, group_b)
            else:
                test_name = "Mann-Whitney U Test"
                stat, p_value = stats.mannwhitneyu(group_a, group_b, alternative='two-sided')

            # Step 3: Effect size (Cohen's d)
            n1, n2 = len(group_a), len(group_b)
            pooled_std = math.sqrt(((n1-1)*group_a.std(ddof=1)**2 + (n2-1)*group_b.std(ddof=1)**2) / (n1+n2-2))
            cohens_d = (group_a.mean() - group_b.mean()) / pooled_std

            st.subheader("Results")
            col1, col2, col3 = st.columns(3)
            col1.metric("Test Used", test_name)
            col2.metric("p-value", f"{p_value:.4f}")
            col3.metric("Effect Size (d)", f"{cohens_d:.4f}")

            # Step 4: Boxplot visual
            st.subheader("Distribution Comparison")
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.boxplot([group_a, group_b], tick_labels=[str(group_a_name), str(group_b_name)])
            ax.set_ylabel(metric_col)
            ax.set_title(f"{metric_col} by group")
            st.pyplot(fig)

            # Step 5: Plain-English verdict
            st.subheader("Verdict")
            if p_value < 0.05:
                st.success(
                    f"**Statistically significant.** There IS a real difference between "
                    f"{group_a_name} and {group_b_name} on {metric_col} (p = {p_value:.4f}). "
                    f"This is unlikely to be due to random chance."
                )
            else:
                st.info(
                    f"**Not statistically significant.** We cannot conclude there's a real "
                    f"difference between {group_a_name} and {group_b_name} on {metric_col} "
                    f"(p = {p_value:.4f}). The observed difference could plausibly be random noise."
                )

            abs_d = abs(cohens_d)
            if abs_d < 0.2:
                effect_desc = "negligible"
            elif abs_d < 0.5:
                effect_desc = "small"
            elif abs_d < 0.8:
                effect_desc = "medium"
            else:
                effect_desc = "large"
            st.caption(f"Effect size interpretation: **{effect_desc}** (|d| = {abs_d:.3f})")