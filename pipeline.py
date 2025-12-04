# pipeline.py

from pathlib import Path

from src.extract import load_default_raw, load_raw_csv
from src.clean import clean_data
from src.validate import validate_data
from src.detect_anomalies import detect_anomalies
from src.visualize import create_visualizations
from src.report import generate_report


def main():
    project_root = Path(__file__).resolve().parent

    # ------------------------------------------------------------------
    # 1) EXTRACT
    # ------------------------------------------------------------------
    print("📥 Step 1/6: Loading raw data...")

    # Option A: use default file in data/wnba_raw.csv
    # df_raw = load_default_raw()

    # Option B: explicitly point to your current CSV
    project_root = Path(__file__).resolve().parent

    raw_path = project_root / "data" / "raw" / "wnba_raw_2024.csv"
    df_raw = load_raw_csv(raw_path)

    print(f"   Loaded {len(df_raw)} rows from {raw_path}")

    # ------------------------------------------------------------------
    # 2) CLEAN
    # ------------------------------------------------------------------
    print("🧹 Step 2/6: Cleaning data...")
    df_clean = clean_data(df_raw)
    print(f"   Cleaning complete. Rows after cleaning: {len(df_clean)}")
        # SAVE CLEANED DATA
    cleaned_path = project_root / "data" / "cleaned" / "wnba_cleaned.csv"
    df_clean.to_csv(cleaned_path, index=False)
    print(f"   Saved cleaned data → {cleaned_path}")

    # ------------------------------------------------------------------
    # 3) VALIDATE
    # ------------------------------------------------------------------
    print("✅ Step 3/6: Validating data...")
    validation_errors = validate_data(df_clean)
    if validation_errors.empty:
        print("   No validation issues found.")
    else:
        print(f"   Validation found {len(validation_errors)} issues.")
        # SAVE VALIDATION ERRORS
    validated_path = project_root / "data" / "validated" / "validation_errors.csv"
    validation_errors.to_csv(validated_path, index=False)
    print(f"   Saved validation errors → {validated_path}")

    # ------------------------------------------------------------------
    # 4) ANOMALY DETECTION
    # ------------------------------------------------------------------
    print("🔍 Step 4/6: Detecting anomalies...")
    anomalies = detect_anomalies(df_clean)
    if anomalies.empty:
        print("   No anomalies detected.")
    else:
        print(f"   Detected {len(anomalies)} anomalous rows.")
        # SAVE ANOMALIES
    anomalies_path = project_root / "data" / "anomalies" / "anomalies.csv"
    anomalies.to_csv(anomalies_path, index=False)
    print(f"   Saved anomalies → {anomalies_path}")

    # ------------------------------------------------------------------
    # 5) VISUALIZATIONS
    # ------------------------------------------------------------------
    print("📊 Step 5/6: Creating visualizations...")
    visuals_dir = project_root / "visuals" / "charts"
    viz_paths = create_visualizations(df_clean, anomalies=anomalies, output_dir=visuals_dir)
    print(f"   Created {len(viz_paths)} chart(s) in {visuals_dir}")

    # ------------------------------------------------------------------
    # 6) REPORT
    # ------------------------------------------------------------------
    print("🧾 Step 6/6: Generating PDF report...")
    reports_dir = project_root / "reports"
    output_pdf = reports_dir / "wnba_data_quality_report.pdf"

    pdf_path = generate_report(
        df_clean=df_clean,
        anomalies=anomalies,
        validation_errors=validation_errors,
        viz_paths=viz_paths,
        output_path=output_pdf,
    )

    print(f"✅ Pipeline complete! Report saved to: {pdf_path}")


if __name__ == "__main__":
    main()