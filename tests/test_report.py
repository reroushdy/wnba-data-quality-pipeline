# tests/test_report.py

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from src.report import generate_report


def _sample_df():
    return pd.DataFrame({
        "player_name": ["A", "B", "C"],
        "team": ["Minnesota Lynx", "Las Vegas Aces", "Atlanta Dream"],
        "points_per_game": [20.0, 26.9, 18.5],
        "games_played": [34, 36, 30],
    })


def test_generate_report_creates_pdf(tmp_path):
    df_clean = _sample_df()
    anomalies = df_clean.iloc[[1]]   # mark one as anomaly
    validation_errors = pd.DataFrame([
        {"row": 0, "column": "team", "severity": "WARNING",
         "code": "INVALID_TEAM", "message": "Mock issue"}
    ])

    # Create a dummy chart to pretend we got it from visualize.create_visualizations
    img_path = tmp_path / "dummy_chart.png"
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.set_title("Dummy Chart")
    fig.savefig(img_path)
    plt.close(fig)

    viz_paths = {"dummy_chart": img_path}

    output_pdf = tmp_path / "wnba_report_test.pdf"

    pdf_path = generate_report(
        df_clean=df_clean,
        anomalies=anomalies,
        validation_errors=validation_errors,
        viz_paths=viz_paths,
        output_path=output_pdf,
    )

    assert pdf_path.exists()
    assert pdf_path.suffix == ".pdf"
    assert pdf_path.stat().st_size > 0  # non-empty file


def test_generate_report_handles_empty_anomalies_and_errors(tmp_path):
    df_clean = _sample_df()
    anomalies = pd.DataFrame(columns=df_clean.columns)
    validation_errors = pd.DataFrame(
        columns=["row", "column", "severity", "code", "message"]
    )

    # Minimal dummy image
    img_path = tmp_path / "dummy_chart.png"
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, "Chart", ha="center", va="center")
    fig.savefig(img_path)
    plt.close(fig)

    viz_paths = {"dummy_chart": img_path}
    output_pdf = tmp_path / "wnba_report_empty_cases.pdf"

    pdf_path = generate_report(
        df_clean=df_clean,
        anomalies=anomalies,
        validation_errors=validation_errors,
        viz_paths=viz_paths,
        output_path=output_pdf,
    )

    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0