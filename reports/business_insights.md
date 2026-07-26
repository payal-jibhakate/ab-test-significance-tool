# 📊 A/B Test Business Insights Report

**Campaign Performance Analysis — Control vs Test (August 2019)**

---

## 📝 Executive Summary

The Test Campaign generated a **~2x higher click-through rate** than Control, but this did not translate into more purchases. After 30 days of testing, there is **no statistically significant difference** in daily purchases between the two campaigns (p = 0.958), and the practical difference is negligible (Cohen's d = 0.008). **Control achieved effectively identical results at a lower cost per purchase ($4.41 vs $4.92).**

> **Recommendation:** Retain the Control campaign creative. Do not roll out the Test campaign as-is — it does not outperform Control on the metric that matters (purchases), and it costs more to run.

---

## 📈 Key Metrics

| Metric | Control | Test | Winner |
|---|---|---|---|
| Total Spend | $66,818 | $76,892 | Control (cheaper) |
| Avg Daily Purchases | 522.8 | 521.2 | No meaningful difference |
| Click-Through Rate | 4.9% | 8.1% | Test |
| Cart Conversion Rate | 24.4% | 14.6% | Control |
| Cost per Purchase | $4.41 | $4.92 | Control |

---

## 🔻 What the Funnel Tells Us

Test's creative is clearly better at generating initial interest — nearly double the click-through rate of Control. But a much larger share of those clickers abandon before adding to cart (Test's cart rate is 40% lower than Control's). In practice, Test attracts more curious browsers while Control attracts more decisive buyers — and the two effects roughly cancel out by the time you reach actual purchases.

**Business implication:** Test's ad creative/targeting may be worth reusing for top-of-funnel awareness goals, but Control's landing/cart experience is doing a better job converting the traffic it gets. A hybrid — Test's ad with Control's post-click experience — is worth testing next, rather than picking one campaign wholesale.

---

## ⚠️ Anomaly Worth Investigating

Both campaigns saw a sharp, synchronized drop in purchases around **August 17–19**, independently confirmed through the EDA time-series chart and the SQL outlier-flagging query. Since both campaigns dropped together, this points to an external factor (platform issue, weekend effect, or an account-level pause) rather than a problem specific to either campaign.

**Recommendation:** Check ad platform status logs or account activity for that window before drawing further conclusions from this data.

---

## 📐 Statistical Confidence

| Check | Result |
|---|---|
| Test Used | Mann-Whitney U |
| Why | Shapiro-Wilk showed Test group data was not normally distributed — a t-test would have violated its own assumptions |
| p-value | 0.958 — far from the 0.05 significance threshold |
| Effect Size | Cohen's d = 0.008 (negligible) — confirms this isn't a case of "not enough data" |

---

## ✅ Recommendations

1. **Do not replace Control with Test** based on this data — no purchase-level improvement, at a higher cost.
2. **Investigate the Aug 17–19 dip** before running further analysis on this period.
3. **Consider a hybrid creative test** — Test's ad copy/targeting + Control's landing experience, to see if combining their strengths beats either campaign alone.