import streamlit as st
import pandas as pd
from scipy import stats
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="A/B Test Significance Tool", layout="centered", page_icon="📊")

st.title("📊 A/B Test Statistical Significance Tool")
st.write("Upload your A/B test data to check if the difference between groups is statistically significant.")

# ---------- SIDEBAR: all inputs live here ----------
with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    df = None
    group_col = metric_col = None

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        group_col = st.selectbox("Group column", df.columns)
        metric_col = st.selectbox("Metric column", df.columns)

# ---------- MAIN AREA: preview + results ----------
if df is not None:
    st.subheader("Data Preview")
    st.dataframe(df.head())

    groups = df[group_col].unique()

    if len(groups) != 2:
        st.warning(f"This tool currently supports exactly 2 groups. Found {len(groups)}: {list(groups)}")
    else:
        group_a_name, group_b_name = groups[0], groups[1]
        group_a = df[df[group_col] == group_a_name][metric_col]
        group_b = df[df[group_col] == group_b_name][metric_col]

        st.success(f"Comparing **{group_a_name}** vs **{group_b_name}** on **{metric_col}**")

        if st.button("Run Significance Test", type="primary"):

            shapiro_a = stats.shapiro(group_a)
            shapiro_b = stats.shapiro(group_b)
            both_normal = shapiro_a.pvalue > 0.05 and shapiro_b.pvalue > 0.05

            if both_normal:
                test_name = "Independent T-Test"
                stat, p_value = stats.ttest_ind(group_a, group_b)
            else:
                test_name = "Mann-Whitney U Test"
                stat, p_value = stats.mannwhitneyu(group_a, group_b, alternative='two-sided')

            n1, n2 = len(group_a), len(group_b)
            pooled_std = math.sqrt(((n1-1)*group_a.std(ddof=1)**2 + (n2-1)*group_b.std(ddof=1)**2) / (n1+n2-2))
            cohens_d = (group_a.mean() - group_b.mean()) / pooled_std

            st.divider()
            st.subheader("Results")
            col1, col2, col3 = st.columns(3)
            col1.metric("Test Used", test_name)
            col2.metric("p-value", f"{p_value:.4f}")
            col3.metric("Effect Size (d)", f"{cohens_d:.4f}")

            st.subheader("Distribution Comparison")
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor("#1E2530")
            ax.set_facecolor("#1E2530")

            box = ax.boxplot([group_a, group_b], tick_labels=[str(group_a_name), str(group_b_name)],
                              patch_artist=True)
            for patch in box['boxes']:
                patch.set_facecolor("#2DD4BF")
                patch.set_alpha(0.6)
            for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
                plt.setp(box[element], color="#FAFAFA")

            ax.set_ylabel(metric_col, color="#FAFAFA")
            ax.set_title(f"{metric_col} by group", color="#FAFAFA")
            ax.tick_params(colors="#FAFAFA")
            for spine in ax.spines.values():
                spine.set_color("#FAFAFA")

            st.pyplot(fig)

            st.divider()
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
else:
    st.info("👈 Upload a CSV file in the sidebar to get started.")