"""Filter-aware PM recommendation generation from descriptive snapshot signals."""
import pandas as pd

from src.metrics import rate_table


def _highest_rate(df: pd.DataFrame, dimension: str) -> pd.Series:
    table = rate_table(df, dimension)
    return table.loc[table["churn_rate"].idxmax()]


def _lowest_activation(df: pd.DataFrame, dimension: str) -> pd.Series:
    table = rate_table(df, dimension)
    return table.loc[table["activation_rate"].idxmin()]


def generate_recommendations(df: pd.DataFrame) -> list[dict[str, str]]:
    """Return recommendations whose evidence and targets change with ``df``.

    These are prioritization hypotheses. The caller must display that they do not
    establish causality in the snapshot source.
    """
    recency_risk = _highest_rate(df, "recency_segment")
    activation_gap = _lowest_activation(df, "viewing_frequency")
    device_risk = _highest_rate(df, "primary_device")

    return [
        {
            "priority": "HIGH",
            "title": "Improve first-session content relevance",
            "evidence": (
                f"{activation_gap['viewing_frequency']} users have the lowest activation proxy "
                f"({activation_gap['activation_rate']:.1%}, n={int(activation_gap['users']):,}) in this filtered view."
            ),
            "target": str(activation_gap["viewing_frequency"]),
            "experiment": "Personalized genre onboarding versus the current generic onboarding.",
            "metric": "First meaningful watch within 24 hours; D7 retention.",
        },
        {
            "priority": "HIGH",
            "title": "Diagnose the highest retention-risk group",
            "evidence": (
                f"{recency_risk['recency_segment']} users have the highest observed churn "
                f"({recency_risk['churn_rate']:.1%}, n={int(recency_risk['users']):,})."
            ),
            "target": str(recency_risk["recency_segment"]),
            "experiment": "Review playback, search, and cancellation journeys; test the strongest discovered friction.",
            "metric": "Churn rate, reactivation rate, and support contacts.",
        },
        {
            "priority": "MEDIUM",
            "title": "Audit the highest-churn device experience",
            "evidence": (
                f"{device_risk['primary_device']} has the highest device-level churn "
                f"({device_risk['churn_rate']:.1%}, n={int(device_risk['users']):,}) in this selection."
            ),
            "target": str(device_risk["primary_device"]),
            "experiment": "Compare content discovery and playback UX with other devices before testing a focused improvement.",
            "metric": "Title-start rate, playback errors, and D7 retention.",
        },
    ]
