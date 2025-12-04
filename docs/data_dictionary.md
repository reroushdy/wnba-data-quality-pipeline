# WNBA Data Pipeline — Data Dictionary

This data dictionary defines every field used in the WNBA analytics pipeline.  
It supports **data cleaning**, **validation**, **database loading**, and **analysis tasks**.

---

## Table of Contents
- [Overview](#overview)
- [Players Table](#players-table)
- [Stats Table](#stats-table)
- [Validation Outputs](#validation-outputs)
- [Anomalies Schema](#anomalies-schema)

---

## Overview

The WNBA dataset combines player information and performance metrics for the  
2024–2025 seasons. It originates from publicly available statistics and is processed  
through a multi-step data pipeline:

1. **Extract** — Load CSV from MySQL export  
2. **Clean** — Standardize names, fix data types, trim whitespace  
3. **Validate** — Confirm schema, ranges, critical fields  
4. **Detect Anomalies** — Identify statistical outliers  
5. **Visualize** — Produce charts  
6. **Report** — Generate PDF summaries

This dictionary ensures all fields have consistent definitions and interpretations.

---

## Players Table

| Column Name      | Type      | Description |
|------------------|-----------|-------------|
| `player_name`     | string    | Full player name as used in league records. |
| `team`            | string    | Full team name (standardized by cleaning). |
| `position`        | string    | Player’s position: G, F, C, G/F, or F/C. |
| `season_year`     | integer   | Season year the stats correspond to. |
| `player_id`       | integer   | Unique identifier assigned for internal reference. |

---

## Stats Table

| Column Name           | Type      | Description |
|-----------------------|-----------|-------------|
| `games_played`        | integer   | Total number of games the player competed in. |
| `points_per_game`     | float     | Average points scored per game. |
| `rebounds_per_game`   | float     | Average rebounds per game. |
| `assists_per_game`    | float     | Average assists per game. |
| `steals_per_game`     | float     | Average steals per game. |
| `blocks_per_game`     | float     | Average blocks per game. |

*All numeric values are validated for range appropriateness (see methodology).*

---

## Validation Outputs

During the validation stage, each issue is represented as a row with:

| Field        | Type     | Meaning |
|--------------|----------|---------|
| `row`        | integer  | Row index containing the error. |
| `column`     | string   | Column where the error was detected. |
| `severity`   | string   | ERROR or WARNING. |
| `code`       | string   | Short, machine-readable error label. |
| `message`    | string   | Human-readable explanation. |

---

## Anomalies Schema

Anomalies (detected via IQR method) include:

| Column              | Type   | Description |
|---------------------|--------|-------------|
| `player_name`       | string | Player flagged due to outlier behavior. |
| `points_per_game`   | float  | Value that triggered the anomaly. |
| `team` (optional)   | string | Included when available in the dataset. |

---

This dictionary should be updated whenever new fields, rules, or datasets are introduced into the pipeline.