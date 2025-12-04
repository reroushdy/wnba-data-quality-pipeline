# src/visualize.py

from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import matplotlib.pyplot as plt


def _find_column(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    """
    Try to find a column in df whose name matches one of the candidates
    (either exact, case-insensitive, or substring match).
    """
    cols = list(df.columns)

    # 1) exact case-insensitive match
    lower_map = {c.lower(): c for c in cols}
    for cand in candidates:
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]

    # 2) substring match
    for cand in candidates:
        for col in cols:
            if cand.lower() in col.lower():
                return col

    return None


def create_visualizations(
    df_clean: pd.DataFrame,
    anomalies: Optional[pd.DataFrame] = None,
    output_dir: str | Path = "visuals",
) -> Dict[str, Path]:
    """
    Create basic visualizations for WNBA stats and save them as PNG files.

    Returns a dict mapping figure names to their file paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_paths: Dict[str, Path] = {}

    # --- figure out which columns to use ---
    team_col = _find_column(df_clean, ["team", "team_name"])
    points_col = _find_column(df_clean, ["points_per_game", "pts", "points"])
    games_col = _find_column(df_clean, ["games_played", "games", "g"])

    print(f"[visualize] Using columns: team={team_col}, points={points_col}, games={games_col}")

    # 1) Bar chart: average points per game by team
    if team_col and points_col:
        fig, ax = plt.subplots(figsize=(8, 5))
        grouped = df_clean.groupby(team_col)[points_col].mean().sort_values()

        grouped.plot(kind="bar", ax=ax)
        ax.set_title("Average Points per Game by Team")
        ax.set_xlabel("Team")
        ax.set_ylabel("Points per Game")
        plt.tight_layout()

        out_path = output_dir / "points_by_team.png"
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        output_paths["points_by_team"] = out_path

    # 2) Histogram: distribution of points per game
    if points_col:
        fig, ax = plt.subplots(figsize=(8, 5))
        df_clean[points_col].plot(kind="hist", bins=10, ax=ax, edgecolor="black")
        ax.set_title("Distribution of Points per Game")
        ax.set_xlabel("Points per Game")
        ax.set_ylabel("Frequency")
        plt.tight_layout()

        out_path = output_dir / "points_distribution.png"
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        output_paths["points_distribution"] = out_path

    # 3) Scatter: points vs games, highlight anomalies if provided
    if points_col and games_col and anomalies is not None and not anomalies.empty:
        # make sure anomalies have the same columns
        if points_col in anomalies.columns and games_col in anomalies.columns:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(
                df_clean[games_col],
                df_clean[points_col],
                alpha=0.6,
                label="Normal",
            )

            ax.scatter(
                anomalies[games_col],
                anomalies[points_col],
                color="red",
                edgecolor="black",
                s=80,
                label="Anomaly",
            )

            ax.set_title("Points vs Games Played (Anomalies Highlighted)")
            ax.set_xlabel("Games Played")
            ax.set_ylabel("Points per Game")
            ax.legend()
            plt.tight_layout()

            out_path = output_dir / "anomalies_scatter.png"
            fig.savefig(out_path, dpi=150)
            plt.close(fig)
            output_paths["anomalies_scatter"] = out_path

    return output_paths