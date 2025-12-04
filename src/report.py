# src/report.py

from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def generate_report(
    df_clean: pd.DataFrame,
    anomalies: Optional[pd.DataFrame],
    validation_errors: Optional[pd.DataFrame],
    viz_paths: Dict[str, Path],
    output_path: str | Path = "reports/wnba_data_quality_report.pdf",
) -> Path:
    """
    Generate a multi-page PDF data quality report.

    - Page 1: summary (row counts, teams, anomalies, validation issues)
    - Additional pages: one per visualization image.

    Returns the Path to the generated PDF.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Normalize None → empty DataFrame
    if anomalies is None:
        anomalies = pd.DataFrame()
    if validation_errors is None:
        validation_errors = pd.DataFrame()

    with PdfPages(output_path) as pdf:
        # -------- Page 1: Text summary --------
        fig, ax = plt.subplots(figsize=(8.5, 11))  # portrait A4-ish
        ax.axis("off")

        n_rows = len(df_clean)
        n_cols = len(df_clean.columns)
        n_teams = df_clean["team"].nunique() if "team" in df_clean.columns else "N/A"
        n_anomalies = len(anomalies)
        n_issues = len(validation_errors)

        lines = [
            "WNBA Data Quality Report",
            "",
            f"Total records: {n_rows}",
            f"Total columns: {n_cols}",
            f"Number of teams: {n_teams}",
            "",
            f"Anomalies detected: {n_anomalies}",
            f"Validation issues: {n_issues}",
        ]

        y = 0.9
        for line in lines:
            ax.text(
                0.1,
                y,
                line,
                fontsize=12 if line else 10,
                transform=ax.transAxes,
                va="top",
                ha="left",
            )
            y -= 0.05 if line else 0.03

        if n_issues > 0:
            ax.text(
                0.1,
                y - 0.02,
                "Example validation issues:",
                fontsize=11,
                transform=ax.transAxes,
                va="top",
                ha="left",
            )
            y -= 0.08
            # Show up to 3 sample issues
            for _, row in validation_errors.head(3).iterrows():
                msg = f"- [{row.get('severity', '')}] {row.get('code', '')}: {row.get('message', '')}"
                ax.text(
                    0.12,
                    y,
                    msg,
                    fontsize=9,
                    transform=ax.transAxes,
                    va="top",
                    ha="left",
                )
                y -= 0.04

        pdf.savefig(fig)
        plt.close(fig)

        # -------- Next pages: charts from viz_paths --------
        for name, img_path in viz_paths.items():
            if not Path(img_path).exists():
                continue

            fig, ax = plt.subplots(figsize=(8.5, 11))
            img = plt.imread(img_path)
            ax.imshow(img)
            ax.axis("off")
            ax.set_title(name.replace("_", " ").title(), fontsize=14)
            pdf.savefig(fig)
            plt.close(fig)

    return output_path