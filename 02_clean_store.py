"""
02_clean_store.py
-----------------
Phase 2: Clean the raw data and store it in a SQLite database.

Reads:  data/raw_world_bank_data.csv   (created by 01_fetch_data.py)
Writes: data/clean_data.csv
        data/bangladesh_development.db  (SQLite database)

Run after 01_fetch_data.py.
"""

import pandas as pd
import os
from sqlalchemy import create_engine, text


def load_and_clean(raw_path="data/raw_world_bank_data.csv"):
    """
    Load the raw long-format CSV, clean it, pivot to wide format,
    and derive additional calculated columns.
    """
    if not os.path.exists(raw_path):
        raise FileNotFoundError(
            f"'{raw_path}' not found. "
            "Please run 01_fetch_data.py first."
        )

    df = pd.read_csv(raw_path)
    print(f"Raw records loaded: {len(df)}")

    # --- Remove exact duplicates (same year + indicator) ---
    before = len(df)
    df = df.drop_duplicates(subset=["year", "indicator"])
    after = len(df)
    if before != after:
        print(f"Dropped {before - after} duplicate rows")

    # --- Pivot: long format -> wide format ---
    # One row per year, one column per indicator
    df_wide = (
        df.pivot(index="year", columns="indicator", values="value")
        .reset_index()
        .sort_values("year")
    )

    # Remove the column index name left by pivot
    df_wide.columns.name = None

    # --- Derived columns ---
    if "GDP_current_USD" in df_wide.columns:
        df_wide["GDP_growth_pct"] = (
            df_wide["GDP_current_USD"].pct_change() * 100
        )
        df_wide["GDP_billions"] = df_wide["GDP_current_USD"] / 1e9

    print(f"Years covered : {int(df_wide['year'].min())} – {int(df_wide['year'].max())}")
    print(f"Columns       : {list(df_wide.columns)}")

    return df_wide


def store_to_database(df, db_path="data/bangladesh_development.db"):
    """
    Write the cleaned wide-format DataFrame to a SQLite database.
    Overwrites any existing table on each run so data stays fresh.
    """
    engine = create_engine(f"sqlite:///{db_path}")

    df.to_sql(
        "development_indicators",
        engine,
        if_exists="replace",   # overwrite on re-run
        index=False,
    )

    print(f"\nDatabase created : {db_path}")
    print(f"Table            : development_indicators ({len(df)} rows)")

    # Quick verification read-back
    with engine.connect() as conn:
        sample = pd.read_sql(
            text(
                "SELECT year, GDP_billions, literacy_rate, internet_users_percent "
                "FROM development_indicators "
                "ORDER BY year DESC "
                "LIMIT 5"
            ),
            conn,
        )
    print("\nMost recent 5 years (sample columns):")
    print(sample.to_string(index=False))


if __name__ == "__main__":
    print("=" * 55)
    print("  Bangladesh Development Dashboard — Phase 2")
    print("  Cleaning data & storing in SQLite")
    print("=" * 55)

    os.makedirs("data", exist_ok=True)

    df = load_and_clean()

    clean_path = "data/clean_data.csv"
    df.to_csv(clean_path, index=False)
    print(f"\nClean CSV saved : {clean_path}")

    store_to_database(df)

    print()
    print("Phase 2 complete. Run 03_visualize.py next.")
