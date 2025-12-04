import pandas as pd
from src.clean import clean_data, DataCleaner


# ------------------------------------------------------
# 1. Test: Standardize Column Names
# ------------------------------------------------------
def test_standardize_column_names():
    raw = pd.DataFrame({
        "Player Name": ["A'ja Wilson"],
        " TEAM ": ["Las Vegas Aces"],
        "points-per-game": [26.9],
        " Rebounds Per Game ": [10.5],
    })

    cleaned = clean_data(raw)

    assert list(cleaned.columns) == [
        "player_name",
        "team",
        "points_per_game",
        "rebounds_per_game",
    ]


# ------------------------------------------------------
# 2. Test: Remove Negative Values (custom cleaning rule)
# ------------------------------------------------------
def test_remove_negative_values():
    dirty = pd.DataFrame({
        "player_name": ["Bad Player", "Good Player"],
        "games_played": [10, 20],
        "points_per_game": [-5.0, 15.0],   # invalid
        "assists_per_game": [2.0, 3.0],
        "rebounds_per_game": [4.0, 5.0],
        "team": ["MIN", "MIN"]
    })

    cleaner = DataCleaner()
    cleaned = cleaner.remove_negative_rows(dirty)   # runs YOUR custom rule

    # Assert the bad row is removed
    assert "Bad Player" not in cleaned["player_name"].values
    assert "Good Player" in cleaned["player_name"].values
    assert len(cleaned) == 1


# ------------------------------------------------------
# 3. Test: Handle Missing Values
# ------------------------------------------------------
def test_handle_missing_values():
    cleaner = DataCleaner()

    df = pd.DataFrame({
        "player_name": ["A'ja Wilson", None, "Napheesa Collier"],
        "points_per_game": [26.9, None, 20.4],
        "team": ["LVA", "MIN", None]
    })

    cleaned = cleaner.handle_missing_values(df)

    # Numeric missing → mean
    mean_ppg = (26.9 + 20.4) / 2
    assert cleaned.loc[1, "points_per_game"] == mean_ppg

    # Text missing → "Unknown"
    assert cleaned.loc[1, "player_name"] == "Unknown"
    assert cleaned.loc[2, "team"] == "Unknown"