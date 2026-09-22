"""Deterministic cleaning and feature engineering for the OTT snapshot dataset."""
from pathlib import Path
import pandas as pd

from src.config import NUMERIC_COLUMNS, REQUIRED_COLUMNS


def validate_source(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df["user_id"].isna().any() or df["user_id"].duplicated().any():
        raise ValueError("user_id must be present and unique.")


def transform_users(df: pd.DataFrame) -> pd.DataFrame:
    """Return a clean copy with transparent, snapshot-safe analytical features."""
    validate_source(df)
    clean = df.copy()
    for column in NUMERIC_COLUMNS:
        clean[column] = pd.to_numeric(clean[column], errors="raise")
    clean["churned_flag"] = clean["churned"].map({"Yes": 1, "No": 0})
    if clean["churned_flag"].isna().any():
        raise ValueError("churned must contain only Yes or No.")

    # A transparent proxy, not a recorded product event.
    clean["activated_proxy"] = (
        (clean["avg_watch_time_minutes"] >= 60)
        & (clean["watch_sessions_per_week"] >= 3)
        & (clean["content_interactions"] >= 5)
    ).astype(int)
    clean["engagement_segment"] = pd.cut(
        clean["avg_watch_time_minutes"],
        bins=[-1, 90, 210, float("inf")],
        labels=["Low watch time", "Medium watch time", "High watch time"],
    ).astype(str)
    clean["recency_segment"] = pd.cut(
        clean["days_since_last_login"],
        bins=[-1, 7, 30, float("inf")],
        labels=["Active (0–7 days)", "At risk (8–30 days)", "Dormant (31+ days)"],
    ).astype(str)
    clean["tenure_cohort"] = pd.cut(
        clean["account_age_months"],
        bins=[0, 6, 12, 24, 36, float("inf")],
        labels=["0–6 months", "7–12 months", "13–24 months", "25–36 months", "37+ months"],
    ).astype(str)
    clean["age_group"] = pd.cut(
        clean["age"], bins=[17, 24, 34, 44, 54, float("inf")],
        labels=["18–24", "25–34", "35–44", "45–54", "55+"],
    ).astype(str)
    clean["viewing_frequency"] = pd.cut(
        clean["watch_sessions_per_week"], bins=[-1, 4, 10, float("inf")],
        labels=["Low (0–4/week)", "Medium (5–10/week)", "High (11+/week)"],
    ).astype(str)
    return clean


def run_pipeline(source: Path, destination: Path) -> pd.DataFrame:
    """Read source without altering it and write the reproducible analytical dataset."""
    cleaned = transform_users(pd.read_csv(source))
    destination.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(destination, index=False)
    return cleaned
