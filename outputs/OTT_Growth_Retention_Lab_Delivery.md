# OTT Growth & Retention Lab — delivery notes

## Dataset audit

- 50,000 users, 19 columns, and 0 missing values.
- `user_id` is unique; no duplicate users were found.
- Churn is 19.9% (9,964 users).
- Numeric fields fall in plausible ranges: age 18–64, account age 1–59 months, watch time 10–299 minutes, and last login 0–59 days.
- The dataset is a **user-level snapshot**. It has no event timestamps, signup date, acquisition channel, marketing cost, experiment variant, or trial/subscription event history.

## What the application measures now

- Churn and behavioral segments
- Recency and tenure-based churn comparisons
- A disclosed behavioral activation proxy
- Device, plan, country, genre, payment, and engagement breakdowns
- An A/B-test hypothesis and sample-size planner

## What it deliberately does not claim

- Recorded event funnel conversion
- D1/D7/D30 retention
- Acquisition-channel performance, CAC, or LTV
- Experiment results or causation

## Run it

1. Install the project dependencies: `pip install -r requirements.txt`.
2. Run the pipeline: `python run_pipeline.py`.
3. Start the app: `streamlit run app.py`.
4. Run verification: `pytest`.

The original CSV is retained as a raw input. The pipeline reads it and writes `data/processed/ott_users_clean.csv` separately.

## Your prompt-by-prompt build guide

Open `docs/CODEX_WORKFLOW.md` in the project. It contains eight sequential, copy-ready prompts for Codex—from dataset audit through the final PM case study—and checkpoints explaining what to review after each one.
