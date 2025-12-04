"""
clean.py  
---------
This module handles the “cleaning” stage of the data pipeline.

Cleaning is NOT validation.
Cleaning is about:
- fixing messy formatting
- normalizing values
- standardizing types
- removing duplicates
- making data structurally consistent

Think of cleaning as:
    “Make the data look right.”

Validation later will handle:
    “Make sure the data IS right.”
"""

import pandas as pd


class DataCleaner:
    """
    Collection of all cleaning operations used by the pipeline.
    """

    # ----------------------------------------------------------
    # Remove negative numeric values
    # ----------------------------------------------------------
    def remove_negative_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        numeric_cols = df.select_dtypes(include="number").columns
        cleaned = df[(df[numeric_cols] >= 0).all(axis=1)]
        return cleaned

    # ----------------------------------------------------------
    # Handle missing values
    # ----------------------------------------------------------
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # Numeric → mean
        numeric_cols = df.select_dtypes(include="number").columns
        for col in numeric_cols:
            if df[col].isna().any():
                df[col].fillna(df[col].mean(), inplace=True)

        # Text → "Unknown"
        object_cols = df.select_dtypes(include="object").columns
        for col in object_cols:
            df[col].fillna("Unknown", inplace=True)

        return df

    # ---------------------------------------------------------
    # 1. STANDARDIZE COLUMN NAMES
    # ---------------------------------------------------------
    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )
        return df

    # ---------------------------------------------------------
    # 2. TRIM WHITESPACE FROM TEXT COLUMNS
    # ---------------------------------------------------------
    def trim_whitespace(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()
        return df

    # ---------------------------------------------------------
    # 3. FIX DATA TYPES
    # ---------------------------------------------------------
    def fix_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except Exception:
                pass
        return df

    # ---------------------------------------------------------
    # 4. STANDARDIZE TEAM NAMES
    # ---------------------------------------------------------
    def normalize_team_names(self, df: pd.DataFrame) -> pd.DataFrame:
        TEAM_MAP = {
            "MIN": "Minnesota Lynx",
            "Min": "Minnesota Lynx",
            "Minnesota": "Minnesota Lynx",
            "Minnesota Lynx": "Minnesota Lynx",

            "LVA": "Las Vegas Aces",
            "LV": "Las Vegas Aces",
            "Las Vegas": "Las Vegas Aces",
            "Las Vegas Aces": "Las Vegas Aces",

            "ATL": "Atlanta Dream",
            "Atlanta": "Atlanta Dream",
            "Atlanta Dream": "Atlanta Dream",
        }

        df = df.copy()
        if "team" in df.columns:
            df["team"] = df["team"].replace(TEAM_MAP)
        if "team_name" in df.columns:
            df["team_name"] = df["team_name"].replace(TEAM_MAP)

        return df

    # ---------------------------------------------------------
    # 5. REMOVE DUPLICATES
    # ---------------------------------------------------------
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        before = len(df)
        df = df.drop_duplicates()
        after = len(df)
        print(f"[clean] Removed {before - after} duplicate rows.")
        return df

    # ---------------------------------------------------------
    # 6. ORCHESTRATE ALL CLEANING STEPS
    # ---------------------------------------------------------
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.standardize_column_names(df)
        df = self.trim_whitespace(df)
        df = self.fix_dtypes(df)
        df = self.normalize_team_names(df)
        df = self.remove_duplicates(df)
        df = self.handle_missing_values(df)
        return df


# ---------------------------------------------------------
# PIPELINE ENTRY POINT
# ---------------------------------------------------------
def clean_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    cleaner = DataCleaner()
    df_cleaned = cleaner.clean(df_raw)
    print(f"[clean] Cleaning complete. Final rows: {len(df_cleaned)}")
    return df_cleaned