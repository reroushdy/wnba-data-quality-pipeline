# WNBA Data Quality Pipeline 🏀

A Python-based **data quality and reporting pipeline** for WNBA player statistics.

This project extracts WNBA stats from a CSV (exported from MySQL), cleans and validates the data, detects statistical anomalies, generates visualizations, and produces a **PDF data quality report** with charts and issue summaries.

It’s designed as a realistic example of how a **Data Quality / QA Engineer** would structure a production-style analytics pipeline.

---

## ✨ Features

- 📥 **Extraction**
  - Loads raw WNBA data from a CSV file (e.g., exported from MySQL Workbench).
  - Centralized loader with basic error handling.

- 🧹 **Cleaning (`src/clean.py`)**
  - Standardizes column names (snake_case, lowercase).
  - Trims whitespace from text fields.
  - Converts numeric-looking columns to numeric types.
  - Normalizes team names (e.g., `LVA` → `Las Vegas Aces`).
  - Removes duplicate rows.
  - Handles missing values:
    - numeric → column mean
    - text → `"Unknown"`

- ✅ **Validation (`src/validate.py`)**
  - Checks required columns exist.
  - Validates numeric ranges (e.g., points_per_game, games_played).
  - Ensures teams and positions use allowed values.
  - Flags missing or “Unknown” critical fields.
  - Detects likely duplicate players.
  - Returns a **DataFrame of validation issues** (with `severity`, `code`, and `message`).

- 🔍 **Anomaly Detection (`src/detect_anomalies.py`)**
  - Uses the **IQR (Interquartile Range)** method to flag statistical outliers.
  - Focuses on `points_per_game` (customizable to other metrics).
  - Produces a filtered DataFrame of anomalous rows.

- 📊 **Visualization (`src/visualize.py`)**
  - Automatically detects suitable columns (e.g., `team` vs `team_name`, `points_per_game` vs `pts`).
  - Generates charts such as:
    - Average points per game by team.
    - Distribution of points per game.
    - Scatterplot highlighting anomalies (when available).
  - Saves PNG charts under `visuals/charts/`.

- 🧾 **PDF Reporting (`src/report.py`)**
  - Builds a multi-page **PDF data quality report** with:
    - Title/summary page.
    - Basic dataset stats.
    - Validation issues summary.
    - Anomalies summary.
    - Embedded charts from `visuals/charts/`.
  - Output saved under `reports/`.

---

## 📂 Project Structure

```text
wnba_data_pipeline/
├── data/
│   ├── raw/          # Raw CSVs (e.g., wnba_raw_2024.csv)
│   ├── cleaned/      # Cleaned exports (wnba_cleaned.csv)
│   ├── anomalies/    # Anomaly CSV outputs
│   └── validated/    # Validation error logs (CSV)
├── docs/
│   ├── data_dictionary.md   # Fields, types, and definitions
│   └── methodology.md       # Pipeline design & methodology
├── reports/
│   └── wnba_data_quality_report.pdf
├── src/
│   ├── clean.py             # Data cleaning logic
│   ├── detect_anomalies.py  # IQR-based anomaly detection
│   ├── extract.py           # CSV loading helpers
│   ├── report.py            # PDF generation
│   ├── validate.py          # Validation rules
│   └── visualize.py         # Plot generation
├── tests/
│   ├── test_clean.py
│   ├── test_validate.py
│   ├── test_anomalies.py
│   ├── test_extract.py
│   ├── test_visualize.py
│   └── test_report.py
├── visuals/
│   ├── charts/      # Generated PNGs from the pipeline
│   └── examples/    # (Optional) Sample or saved visuals
├── pipeline.py      # Main orchestration script
├── requirements.txt
└── README.md

---

## 🧪 Tests
Unit tests are implemented with pytest and cover:
	•	Cleaning behavior (DataCleaner)
	•	Validation rules (DataValidator)
	•	Anomaly detection
	•	Visualization outputs (basic existence, not aesthetics)
	•	Extraction error handling
	•	Report generation (PDF file exists)

---

## 🔮 Possible Enhancements (Future Work)
	•	Add a data quality score (0–100) based on:
	•	validation errors
	•	warnings
	•	anomaly counts
	•	Support multiple seasons and trend analysis.
	•	Add database integration (e.g., load cleaned data into MySQL/PostgreSQL).
	•	Containerize with Docker for reproducible environments.
	•	Build a dashboard using Streamlit / Power BI / Tableau.

---

## 🎯 Why This Project Matters
This project demonstrates:
	•	How a QA / Data Quality Engineer thinks about data robustness.
	•	How to combine:
	•	Python (pandas, matplotlib)
	•	testing (pytest)
	•	reporting (ReportLab)
	•	and structured directories
	•	How to turn raw sports data into an auditable, tested data product.
It’s suitable as a portfolio project to showcase skills in:
	•	data quality engineering
	•	Python scripting
	•	data validation & anomaly detection
	•	basic reporting & visualization pipelines

