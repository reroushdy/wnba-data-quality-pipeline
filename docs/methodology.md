# WNBA Data Pipeline — Methodology

This document describes the full data pipeline architecture  
used to clean, validate, analyze, and report on WNBA player statistics.

---

## Pipeline Overview

The pipeline follows six major stages:

1. **Extract**
2. **Clean**
3. **Validate**
4. **Detect Anomalies**
5. **Visualize**
6. **Generate Report**

Each stage has been implemented with its own module inside `src/`.

---

## 1. Extract Phase

The extract step loads raw CSVs exported from MySQL Workbench.

Goals:
- Read CSV safely with error handling
- Fail gracefully on missing/empty files
- Maintain a single centralized loading function

Important behavior:
- Empty files raise a `ValueError`
- The default raw file lives under: `data/raw/`
- `extract.py` also supports local paths for future API ingestion

---

## 2. Clean Phase

Cleaning focuses on **fixing formatting**, not business logic.

### Cleaning Actions
- Standardize column names (lowercase, snake_case)
- Trim whitespace
- Convert numeric strings to numeric types
- Normalize team names (LVA → Las Vegas Aces)
- Remove duplicate rows
- Fill missing numeric values with column means
- Fill missing text values with `"Unknown"`

Outcome:  
A consistent, analysis-ready DataFrame.

---

## 3. Validation Phase

Validation ensures the cleaned data *makes sense*.

### What We Check
- Required columns exist
- Numeric values are within realistic bounds
- Teams and positions match known allowed sets
- Missing critical fields are flagged
- Duplicate players are detected
- Dataset-wide structural issues are reported

Validation results are returned as a **DataFrame of issues**.

---

## 4. Anomaly Detection Phase

The pipeline uses the **IQR method** to find outliers.

### Method
Compute Q1 and Q3 → find the interquartile range (IQR):