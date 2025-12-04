import pandas as pd
from src.detect_anomalies import detect_anomalies

def test_detects_high_outlier():
    df = pd.DataFrame({
        "player_name": ["A", "B", "C"],
        "points_per_game": [20, 22, 100],  # 100 is an outlier
    })

    anomalies = detect_anomalies(df)

    assert len(anomalies) == 1
    assert anomalies.iloc[0]["player_name"] == "C"


def test_returns_empty_when_no_outliers():
    df = pd.DataFrame({
        "player_name": ["A", "B", "C"],
        "points_per_game": [20, 21, 22],
    })

    anomalies = detect_anomalies(df)

    assert anomalies.empty