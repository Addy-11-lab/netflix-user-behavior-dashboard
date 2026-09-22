from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT / "data" / "raw" / "netflix_user_behavior_dataset.csv"
PROCESSED_DATA_PATH = ROOT / "data" / "processed" / "ott_users_clean.csv"

REQUIRED_COLUMNS = {
    "user_id", "age", "gender", "country", "account_age_months",
    "subscription_type", "monthly_fee", "payment_method", "primary_device",
    "devices_used", "favorite_genre", "avg_watch_time_minutes",
    "watch_sessions_per_week", "binge_watch_sessions", "completion_rate",
    "rating_given", "content_interactions", "recommendation_click_rate",
    "days_since_last_login", "churned",
}

NUMERIC_COLUMNS = {
    "age", "account_age_months", "monthly_fee", "devices_used",
    "avg_watch_time_minutes", "watch_sessions_per_week", "binge_watch_sessions",
    "completion_rate", "rating_given", "content_interactions",
    "recommendation_click_rate", "days_since_last_login",
}
