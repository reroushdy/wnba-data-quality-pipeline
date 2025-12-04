# tests/test_extract.py

import pandas as pd
import pytest
from pathlib import Path

from src.extract import load_raw_csv


def test_load_raw_csv_reads_data(tmp_path):
    """Happy path: CSV loads correctly into a DataFrame."""
    csv_path = tmp_path / "sample_players.csv"

    original = pd.DataFrame({
        "player_name": ["A'ja Wilson", "Napheesa Collier"],
        "team": ["Las Vegas Aces", "Minnesota Lynx"],
        "points_per_game": [26.9, 20.4],
    })
    original.to_csv(csv_path, index=False)

    df = load_raw_csv(csv_path)

    assert list(df.columns) == list(original.columns)
    assert len(df) == 2
    assert set(df["player_name"]) == {"A'ja Wilson", "Napheesa Collier"}


def test_load_raw_csv_missing_file_raises():
    """Trying to load a non-existent file should give a clean error."""
    with pytest.raises(FileNotFoundError):
        load_raw_csv("this_file_does_not_exist.csv")


def test_load_raw_csv_empty_file_raises(tmp_path):
    """Empty CSV should not silently pass through the pipeline."""
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("")  # create an empty file

    with pytest.raises(ValueError):
        load_raw_csv(csv_path)