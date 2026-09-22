# Building this project with Codex: a sequential workflow

Use one prompt at a time. Review the change, run the requested check, and commit only when you understand it. Replace `[PATH_TO_DATASET]` with the file location on your computer. Never ask Codex to invent missing columns or results.

## 0. Start the workspace

Create a new empty folder, open it in Codex, then use:

```text
I am building a portfolio project called “OTT Growth & Retention Lab” for Growth PM roles. Use Python and Streamlit. Create a clean project skeleton with app.py, src/, tests/, data/raw/, data/processed/, docs/, requirements.txt, .gitignore, and README.md. The raw source must remain unmodified and must not be committed. Do not add analytics pages yet. Explain the structure after creating it.
```

## 1. Inspect before designing

```text
Inspect the CSV at [PATH_TO_DATASET] without modifying it. Report: row count, column names, inferred types, null counts, duplicate user IDs, categorical distributions, numeric min/median/max, and invalid ranges. Then classify which of these are actually supported: funnel, signup cohort retention, churn, segmentation, acquisition-channel analysis, and A/B-test analysis. Do not infer dates, events, channels, or experiment groups that are not present. Save a concise assessment to docs/DATA_AUDIT.md.
```

**Your review checkpoint:** the project must say “snapshot” if there are no timestamps/events. Do not let the app call a behavioral proxy a real funnel.

## 2. Build the reproducible data pipeline

```text
Create a reproducible pipeline. It must read data/raw/netflix_user_behavior_dataset.csv, validate the source schema and unique user_id values, and write a separate cleaned file to data/processed/ott_users_clean.csv. Keep the transformation functions small and testable. Add only transparent derived fields: churned_flag, recency segment, watch-time engagement segment, tenure cohort, and an activation_proxy based on documented thresholds. Do not overwrite the raw file. Add pytest tests for successful transformation and duplicate-ID rejection. Update the README with run commands.
```

**Run:** `python run_pipeline.py`, then `pytest`.

## 3. Define metrics before building charts

```text
Read the pipeline and dataset audit. Write docs/METRICS.md defining every metric, its numerator, denominator, unit, caveat, and decision it informs. Include churn rate, activation proxy, recency, tenure cohort, and a behavioral funnel proxy. Add a “Not measurable from this dataset” section for calendar retention, attribution, CAC, LTV, and causal experiment effects. Keep the writing suitable for a PM portfolio.
```

## 4. Build the MVP dashboard

```text
Build a polished Streamlit dashboard using the processed dataset. Use a dark-neutral or clean editorial visual style, but prioritize readability. Add filters for country, subscription plan, and primary device. Add tabs: Overview, Funnel, Tenure & churn, Segments, Acquisition, Experiment lab, and PM brief. Use Plotly charts. Every unsupported analysis must be shown as an instrumentation gap, not a made-up chart. Ensure empty filter results are handled safely. Do not add authentication, databases, or APIs.
```

**Run:** `streamlit run app.py`; check every filter and tab.

## 5. Make the recommendations defensible

```text
Audit the app’s copy and recommendations for analytical honesty. Each recommendation must label what is observed in the snapshot, what is a hypothesis, and what data would validate it. Add a focused experiment recommendation around first-session content relevance/personalized onboarding. Include a primary metric, guardrails, segmentation target, decision rule, and the minimal events required to measure the result. Do not claim causation from the snapshot.
```

## 6. Add a proper event-tracking plan

```text
Create docs/EVENT_TRACKING_PLAN.md for an OTT product. Include an event dictionary with signup_started, signup_completed, app_opened, onboarding_completed, content_impression, title_started, watch_10_minutes, trial_started, subscription_started, renewal_completed, cancellation_started, and cancellation_completed. For each event list when it fires, key properties, and why it matters. Include user_id, event_timestamp, session_id, acquisition_channel, campaign_id, platform, app_version, and experiment_variant where applicable. Define real activation and D1/D7/D30 retention from those events.
```

## 7. Production-quality pass

```text
Review this repository as a senior analytics engineer and Growth PM. Fix concrete reliability, accessibility, and copy issues. Run the tests. Confirm that the raw data is ignored, the pipeline is reproducible, all metrics have definitions, and unsupported analyses are clearly disclosed. Summarize only the changes made and any remaining measurement limitations.
```

## 8. Create the portfolio case study

```text
Using docs/PM_CASE_STUDY.md as the outline, draft a concise portfolio case study for this project. Use the actual dataset facts and describe missing instrumentation as a product discovery insight. Write in first person, distinguish data findings from hypotheses, and include: problem, user, north-star metric, metric tree, analysis, key insight, proposed experiment, measurement plan, prioritization, and next steps. Do not fabricate interviews, outcomes, or business impact.
```

## How to use Codex well

1. Paste a single prompt above.
2. Let Codex make the scoped change.
3. Read the diff before accepting it; ask “why is this metric valid?” whenever a number is introduced.
4. Run the command under each checkpoint yourself.
5. Keep a screenshot after each finished dashboard page for the case study.
6. Commit in small milestones: scaffold, pipeline, metrics, dashboard, PM layer.
