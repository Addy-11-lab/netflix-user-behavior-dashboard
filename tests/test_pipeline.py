import pandas as pd
import pytest

from src.pipeline import transform_users


def sample_data():
    return pd.DataFrame({
        "user_id": ["u1", "u2"], "age": [25, 31], "gender": ["Male", "Female"],
        "country": ["India", "USA"], "account_age_months": [4, 18],
        "subscription_type": ["Basic", "Premium"], "monthly_fee": [7.99, 15.99],
        "payment_method": ["UPI", "Credit Card"], "primary_device": ["Mobile", "TV"],
        "devices_used": [1, 2], "favorite_genre": ["Comedy", "Drama"],
        "avg_watch_time_minutes": [70, 250], "watch_sessions_per_week": [3, 8],
        "binge_watch_sessions": [1, 4], "completion_rate": [50, 90],
        "rating_given": [4, 5], "content_interactions": [5, 20],
        "recommendation_click_rate": [40, 75], "days_since_last_login": [2, 35],
        "churned": ["No", "Yes"],
    })


def test_transform_adds_analytical_features_without_mutating_input():
    source = sample_data()
    result = transform_users(source)
    assert {"churned_flag", "activated_proxy", "tenure_cohort", "age_group", "viewing_frequency"} <= set(result.columns)
    assert "churned_flag" not in source.columns
    assert result["churned_flag"].tolist() == [0, 1]


def test_transform_rejects_duplicate_user_ids():
    bad = sample_data()
    bad.loc[1, "user_id"] = "u1"
    with pytest.raises(ValueError, match="unique"):
        transform_users(bad)
