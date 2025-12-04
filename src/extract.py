# src/extract.py

from pathlib import Path
import pandas as pd


def load_raw_csv(path: str | Path) -> pd.DataFrame:
    """
    Load a raw CSV file into a pandas DataFrame.

    - Raises FileNotFoundError if the file doesn't exist.
    - Raises ValueError if the file exists but is empty.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file '{path}': {e}") from e

    if df.empty:
        raise ValueError(f"CSV file '{path}' is empty.")

    return df


def load_default_raw() -> pd.DataFrame:
    """
    Convenience helper: load the 'default' WNBA raw data file.

    Assumes a file at:  project_root / data / wnba_raw.csv

    You can change this path to whatever you actually use.
    """
    project_root = Path(__file__).resolve().parents[1]
    default_path = project_root / "data" / "wnba_raw.csv"
    return load_raw_csv(default_path)