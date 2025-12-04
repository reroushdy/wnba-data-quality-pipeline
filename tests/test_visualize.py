# tests/test_visualize.py

from pathlib import Path
import pandas as pd

from src.visualize import create_visualizations


def _sample_df():
    return pd.DataFrame({
        "player_name": ["A", "B", "C", "D"],
        "team": ["Minnesota Lynx", "Minnesota Lynx", "Las Vegas Aces", "Atlanta Dream"],
        "points_per_game": [20.0, 22.0, 26.9, 18.5],
        "games_played": [34, 32, 36, 30],
    })


def test_create_visualizations_creates_files(tmp_path):
    df = _sample_df()

    output_paths = create_visualizations(df, anomalies=None, output_dir=tmp_path)

    # We expect at least these two plots, plus possibly a third for anomalies
    assert "points_by_team" in output_paths
    assert "points_distribution" in output_paths

    for name, path in output_paths.items():
        assert isinstance(path, Path)
        assert path.exists()
        assert path.suffix == ".png"


def test_create_visualizations_with_anomalies(tmp_path):
    df = _sample_df()
    # mark one row as anomalous
    anomalies = df.iloc[[2]]  # just player C

    output_paths = create_visualizations(df, anomalies=anomalies, output_dir=tmp_path)

    # When anomalies are provided, we should also get a scatter plot
    assert "anomalies_scatter" in output_paths
    scatter_path = output_paths["anomalies_scatter"]
    assert scatter_path.exists()
    assert scatter_path.suffix == ".png"