import pandas as pd
import numpy as np

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Hybrid anomaly detector:
    - IQR rule for larger data sets
    - Z-score rule for larger data sets
    - Median distance rule for tiny data sets (<5 rows)
    """
    if df.empty:
        return df.copy()

    numeric_cols = df.select_dtypes(include="number").columns
    anomaly_mask = pd.Series(False, index=df.index)

    for col in numeric_cols:
        col_data = df[col].dropna()
        n = len(col_data)

        # Basic rule for very small samples
        if n < 5:
            med = np.median(col_data)
            diffs = np.abs(col_data - med)
            # If there are at least 2 points, compare largest diff to second largest
            if len(diffs) > 1:
                sorted_diffs = np.sort(diffs)
                if sorted_diffs[-1] > 3 * sorted_diffs[-2]:
                    outlier_idx = diffs.idxmax()
                    anomaly_mask[outlier_idx] = True
            continue

        # Otherwise use IQR and Z-score rules
        q1, q3 = col_data.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
        iqr_mask = (df[col] < lower) | (df[col] > upper)

        mean = col_data.mean()
        std  = col_data.std(ddof=0)
        z_mask = pd.Series(False, index=df.index)
        if std > 0:
            z_scores = (df[col] - mean) / std
            # Use a moderate threshold so extreme values in larger sets are flagged
            z_mask = z_scores.abs() > 2.0

        anomaly_mask |= iqr_mask | z_mask

    return df[anomaly_mask].copy()