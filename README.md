# Netflix User Behavior Analytics

A polished Streamlit product-analytics dashboard for understanding user behavior, identifying churn risk, and designing the next growth experiment. It is built as a portfolio project for Product Manager, Growth PM, and Product Analyst roles.

> **Live local app:** run `streamlit run app.py` and open the URL Streamlit displays.

## Product questions answered

- Which users are most engaged, and on which devices?
- Which plans, genres, and viewing-frequency segments have the strongest engagement signals?
- Where is churn concentrated across recency, device, plan, country, genre, and payment method?
- What should a PM investigate next—and what experiment and metric would validate the decision?

## Dashboard experience

- Premium Netflix-inspired dark interface with responsive KPI cards
- Resettable filters for country, age group, gender, plan, device, favorite genre, and viewing frequency
- Dynamic executive summary that updates with every selection
- Filter-aware PM recommendations: evidence, target segment, experiment, and success metric recalculate from the current view
- Tooltips, empty states, sample sizes, and transparent metric definitions
- A/B-test planner for activation experiments

## What this project demonstrates

- Funnel thinking with an explicitly labeled behavioral activation proxy
- Tenure-based churn comparisons and retention measurement design
- Churn segmentation by device, plan, country, genre, engagement, and recency
- Honest acquisition-channel and experiment-readiness gap analysis
- A/B-test hypothesis, primary metric, guardrails, and sample-size estimate
- Product recommendations that distinguish observation, hypothesis, and decision


## Dataset assessment

The supplied CSV has 50,000 records, 19 columns, unique user IDs, no missing values, and valid numeric ranges. It contains a user-level snapshot—not event timestamps, signup dates, acquisition channel, trial state, or experiment variant.

Therefore, this MVP **does not fabricate** an event funnel, D1/D7/D30 retention, acquisition attribution, or experiment outcome. It visualizes a documented activation proxy and shows the required instrumentation to answer those questions correctly.

| Available now | Requires new data |
|---|---|
| Churn rate, engagement and recency segments | True visit → signup → trial → subscribe funnel |
| Plan/device/country/genre comparison | Signup cohorts and D1/D7/D30 retention |
| Tenure cohort churn | CAC/LTV by acquisition channel |
| Experiment plan and sample estimate | A/B test results and causal claims |

## Quick start

1. Create and activate a virtual environment.
2. Run `pip install -r requirements.txt`.
3. Copy (do not move or edit) the original dataset to `data/raw/netflix_user_behavior_dataset.csv`.
4. Run `python run_pipeline.py` to create `data/processed/ott_users_clean.csv`.
5. Run `streamlit run app.py`.
6. Run `pytest` before presenting or deploying.


## Project structure

```text
app.py                  # Streamlit product analytics app
data/raw/               # original, immutable input (not committed)
data/processed/         # reproducible derived dataset (not committed)
src/pipeline.py         # validation and feature engineering
src/metrics.py          # reusable metric definitions
tests/                  # pipeline tests
docs/                   # PM artifacts and delivery prompts
```

## Metric definitions

- **Churn rate:** users marked `churned = Yes` / users in segment.
- **Activation proxy:** watch time ≥60 minutes, ≥3 sessions/week, and ≥5 content interactions. It is a project assumption, not a logged activation event.
- **Recency:** 0–7 active, 8–30 at risk, and 31+ dormant days since last login.
- **Tenure cohort:** buckets of `account_age_months`; it is not a calendar signup cohort.


## Tech stack

Python · Streamlit · Pandas · Plotly · SciPy · Pytest
