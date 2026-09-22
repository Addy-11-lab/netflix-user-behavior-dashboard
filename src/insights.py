"""Dynamic, descriptive product insights generated only from the displayed data."""
import pandas as pd

from src.metrics import rate_table


def highest_churn_segment(df: pd.DataFrame, dimension: str) -> pd.Series:
    table = rate_table(df, dimension)
    return table.loc[table["churn_rate"].idxmax()]


def executive_summary(df: pd.DataFrame) -> list[str]:
    recency = highest_churn_segment(df, "recency_segment")
    device = highest_churn_segment(df, "primary_device")
    engagement = rate_table(df, "engagement_segment").sort_values("avg_watch_minutes", ascending=False).iloc[0]
    return [
        f"**Retention risk:** {recency['recency_segment']} users have the highest observed churn ({recency['churn_rate']:.1%}, n={int(recency['users']):,}).",
        f"**Segment to investigate:** {device['primary_device']} has the highest device-level churn ({device['churn_rate']:.1%}, n={int(device['users']):,}).",
        f"**Engagement pattern:** {engagement['engagement_segment']} users average {engagement['avg_watch_minutes']:.0f} watch minutes; compare their discovery journey with lower-engagement users.",
    ]
