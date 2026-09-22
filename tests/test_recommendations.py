from src.pipeline import transform_users
from src.recommendations import generate_recommendations
from tests.test_pipeline import sample_data


def test_recommendations_are_built_from_the_filtered_data():
    data = transform_users(sample_data())
    cards = generate_recommendations(data[data["primary_device"] == "TV"])
    assert len(cards) == 3
    assert "TV" in cards[2]["evidence"]
    assert "n=1" in cards[0]["evidence"]
