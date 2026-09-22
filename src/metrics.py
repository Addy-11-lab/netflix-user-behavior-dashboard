"""Metrics helpers. All rates use a user as the unit of analysis."""
import pandas as pd


def rate_table(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    table = df.groupby(dimension, dropna=False).agg(
        users=("user_id", "nunique"),
        churn_rate=("churned_flag", "mean"),
        activation_rate=("activated_proxy", "mean"),
        avg_watch_minutes=("avg_watch_time_minutes", "mean"),
        avg_sessions_per_week=("watch_sessions_per_week", "mean"),
    ).reset_index()
    return table.sort_values("users", ascending=False)


def proxy_funnel(df: pd.DataFrame) -> pd.DataFrame:
    """Behavioral funnel inferred from snapshot variables; not a logged event funnel."""
    thresholds = [
        ("Dataset users", pd.Series(True, index=df.index)),
        ("Engaged: 1+ session/week", df["watch_sessions_per_week"] >= 1),
        ("Watched 60+ min", df["avg_watch_time_minutes"] >= 60),
        ("Interacted 5+ times", df["content_interactions"] >= 5),
        ("Activated proxy", df["activated_proxy"] == 1),
    ]
    rows, prior = [], None
    for stage, condition in thresholds:
        users = int(condition.sum())
        rows.append({
            "stage": stage,
            "users": users,
            "rate_from_all": users / len(df),
            "step_conversion": None if prior is None else users / prior,
        })
        prior = users
    return pd.DataFrame(rows)


def top_churn_segments(df: pd.DataFrame, dimension: str, min_users: int = 100) -> pd.DataFrame:
    table = rate_table(df, dimension)
    return table[table["users"] >= min_users].sort_values("churn_rate", ascending=False)
