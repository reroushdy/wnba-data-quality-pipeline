"""
validate.py
-----------
Validation layer for the WNBA data pipeline.

Cleaning = make data look right.
Validation = make sure data IS right.

This module checks:
- schema / required columns
- numeric ranges
- allowed values (teams, positions)
- missing critical fields
- duplicates
and returns a structured list/DataFrame of validation errors.
"""

from typing import List, Optional
import pandas as pd


class DataValidator:
    """
    Performs structural, business, and consistency checks
    on the CLEANED DataFrame.

    Usage:
        validator = DataValidator()
        errors = validator.validate(df_clean)
    """

    def __init__(self):
        # each error is a dict: {row, column, severity, code, message}
        self.errors: List[dict] = []

    # ----------------------------------------------------------
    # Helper: record an error
    # ----------------------------------------------------------
    def add_error(
        self,
        *,
        code: str,
        message: str,
        severity: str = "ERROR",
        row: Optional[int] = None,
        column: Optional[str] = None,
    ):
        self.errors.append(
            {
                "row": row,
                "column": column,
                "severity": severity,
                "code": code,
                "message": message,
            }
        )

    # ----------------------------------------------------------
    # 1. REQUIRED COLUMNS
    # ----------------------------------------------------------
    def check_required_columns(self, df: pd.DataFrame):
        required = [
            "player_name",
            "team",
            "points_per_game",
            "games_played",
        ]

        for col in required:
            if col not in df.columns:
                self.add_error(
                    code="MISSING_COLUMN",
                    message=f"Missing required column: {col}",
                    column=col,
                    row=None,
                    severity="ERROR",
                )

    # ----------------------------------------------------------
    # 2. NUMERIC RANGE CHECKS
    # ----------------------------------------------------------
    def check_numeric_ranges(self, df: pd.DataFrame):
        """
        Check that numeric values fall in realistic ranges.
        You can expand these rules as the model evolves.
        """
        rules = {
            "points_per_game": {"min": 0, "max": 60},
            "assists_per_game": {"min": 0, "max": 20},
            "rebounds_per_game": {"min": 0, "max": 30},
            "games_played": {"min": 0, "max": 50},  # WNBA seasons are short
        }

        for col, bounds in rules.items():
            if col not in df.columns:
                continue

            min_val = bounds["min"]
            max_val = bounds["max"]

            for idx, value in df[col].items():
                # skip NaNs — missingness is handled elsewhere
                if pd.isna(value):
                    continue
                try:
                    v = float(value)
                except Exception:
                    self.add_error(
                        code="INVALID_NUMERIC",
                        message=f"Non-numeric value in numeric field '{col}': {value!r}",
                        row=idx,
                        column=col,
                        severity="ERROR",
                    )
                    continue

                if v < min_val or v > max_val:
                    self.add_error(
                        code="OUT_OF_RANGE",
                        message=f"Value {v} in '{col}' outside [{min_val}, {max_val}]",
                        row=idx,
                        column=col,
                        severity="ERROR",
                    )

    # ----------------------------------------------------------
    # 3. ALLOWED CATEGORICAL VALUES
    # ----------------------------------------------------------
    def check_allowed_values(self, df: pd.DataFrame):
        """
        Ensure that categorical values come from a known set.
        """

        # Known teams — you can expand this as you add more
        allowed_teams = {
            "Minnesota Lynx",
            "Las Vegas Aces",
            "Atlanta Dream",
        }

        if "team" in df.columns:
            for idx, value in df["team"].items():
                if pd.isna(value):
                    continue
                if value not in allowed_teams:
                    self.add_error(
                        code="INVALID_TEAM",
                        message=f"Unknown team: {value}",
                        row=idx,
                        column="team",
                        severity="WARNING",  # could be ERROR if you want stricter rules
                    )

        # Allowed player positions (basic model)
        allowed_positions = {"G", "F", "C", "G/F", "F/C"}

        if "position" in df.columns:
            for idx, value in df["position"].items():
                if pd.isna(value):
                    continue
                if value not in allowed_positions:
                    self.add_error(
                        code="INVALID_POSITION",
                        message=f"Unexpected position value: {value}",
                        row=idx,
                        column="position",
                        severity="WARNING",
                    )

    # ----------------------------------------------------------
    # 4. MISSING CRITICAL VALUES
    # ----------------------------------------------------------
    def check_missing_critical_values(self, df: pd.DataFrame):
        """
        Check that critical fields like player_name and team are present
        and not left as 'Unknown' after cleaning.
        """
        for idx, row in df.iterrows():

            if "player_name" in df.columns:
                name = row["player_name"]
                if pd.isna(name) or str(name).strip() == "" or str(name) == "Unknown":
                    self.add_error(
                        code="MISSING_PLAYER_NAME",
                        message="Missing or Unknown player_name",
                        row=idx,
                        column="player_name",
                        severity="ERROR",
                    )

            if "team" in df.columns:
                team = row["team"]
                if pd.isna(team) or str(team).strip() == "":
                    self.add_error(
                        code="MISSING_TEAM",
                        message="Missing team value",
                        row=idx,
                        column="team",
                        severity="ERROR",
                    )

    # ----------------------------------------------------------
    # 5. DUPLICATE CHECKS
    # ----------------------------------------------------------
    def check_duplicates(self, df: pd.DataFrame):
        """
        Check for duplicate players (simplified).
        """

        # EARLY EXIT — this fixes your KeyError
        if "team" not in df.columns:
            return

        if "player_name" not in df.columns:
            return

        dup_mask = df.duplicated(subset=["player_name", "team"], keep=False)
        duplicated_rows = df[dup_mask]

        for idx, row in duplicated_rows.iterrows():
            self.add_error(
                code="DUPLICATE_PLAYER",
                message=f"Duplicate player/team combination: {row['player_name']} / {row.get('team')}",
                row=idx,
                column=None,
                severity="WARNING",
            )

    # ----------------------------------------------------------
    # 6. DATASET-LEVEL CHECKS
    # ----------------------------------------------------------
    def check_dataset_level(self, df: pd.DataFrame):
        """
        Global dataset checks.
        """
        if len(df) == 0:
            self.add_error(
                code="EMPTY_DATASET",
                message="DataFrame is empty after cleaning.",
                row=None,
                column=None,
                severity="ERROR",
            )
            return

        if "team" in df.columns and "player_name" in df.columns:
            counts = df.groupby("team")["player_name"].nunique()
            for team, count in counts.items():
                if count > 20:
                    self.add_error(
                        code="TOO_MANY_PLAYERS",
                        message=f"Team '{team}' has {count} unique players (too high).",
                        row=None,
                        column="team",
                        severity="WARNING",
                    )

    # ----------------------------------------------------------
    # MAIN VALIDATION ORCHESTRATOR
    # ----------------------------------------------------------
    def validate(self, df: pd.DataFrame) -> List[dict]:
        self.errors = []

        self.check_required_columns(df)
        self.check_numeric_ranges(df)
        self.check_allowed_values(df)
        self.check_missing_critical_values(df)
        self.check_duplicates(df)
        self.check_dataset_level(df)

        return self.errors


# ----------------------------------------------------------
# PIPELINE-FACING HELPER
# ----------------------------------------------------------
def validate_data(df_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Wrapper for pipeline integration.
    Returns a DataFrame of validation errors.
    """
    validator = DataValidator()
    errors = validator.validate(df_clean)

    if not errors:
        print("[validate] No validation errors found ✅")
        return pd.DataFrame(columns=["row", "column", "severity", "code", "message"])

    errors_df = pd.DataFrame(errors)
    print(f"[validate] Validation completed with {len(errors_df)} issues.")
    return errors_df