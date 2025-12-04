import pandas as pd
from src.validate import DataValidator, validate_data


def test_missing_required_columns():
    df = pd.DataFrame({
        "player_name": ["A'ja Wilson"],
        # team column missing on purpose
    })

    validator = DataValidator()
    errors = validator.validate(df)

    assert any(e["code"] == "MISSING_COLUMN" and e["column"] == "team" for e in errors)


def test_numeric_range_validation():
    df = pd.DataFrame({
        "player_name": ["Bad Shooter"],
        "team": ["Minnesota Lynx"],
        "points_per_game": [120],  # impossible
        "games_played": [10],
    })

    validator = DataValidator()
    errors = validator.validate(df)

    assert any(e["code"] == "OUT_OF_RANGE" and e["column"] == "points_per_game" for e in errors)


def test_allowed_team_values():
    df = pd.DataFrame({
        "player_name": ["Test Player"],
        "team": ["Mars Meteors"],  # not in allowed list
        "points_per_game": [10],
        "games_played": [5],
    })

    validator = DataValidator()
    errors = validator.validate(df)

    assert any(e["code"] == "INVALID_TEAM" for e in errors)


def test_no_errors_for_good_data():
    df = pd.DataFrame({
        "player_name": ["A'ja Wilson"],
        "team": ["Las Vegas Aces"],
        "points_per_game": [26.9],
        "games_played": [30],
    })

    errors_df = validate_data(df)
    assert errors_df.empty