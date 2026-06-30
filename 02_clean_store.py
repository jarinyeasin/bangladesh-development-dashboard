import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import os

def load_and_clean():
    """Load raw data and clean it"""
    df = pd.read_csv("data/raw_world_bank_data.csv")
    
    # Check for duplicates
    print(f"Raw records: {len(df)}")
    df = df.drop_duplicates(subset=["year", "indicator"])
    print(f"After deduplication: {len(df)}")
    
    # Pivot to wide format - one row per year, 
    # one column per indicator
    df_wide = df.pivot(
        index="year", 
        columns="indicator", 
        values="value"
    ).reset_index()
    
    # Sort by year
    df_wide = df_wide.sort_values("year")
    
    # Calculate year-on-year GDP growth
    if "GDP_current_USD" in df_wide.columns:
        df_wide["GDP_growth_pct"] = df_wide["GDP_current_USD"].pct_change() * 100
    
    print(f"\nYears covered: {df_wide['year'].min()} to {df_wide['year'].max()}")
    print(f"Columns: {list(df_wide.columns)}")
    
    return df_wide

def store_to_database(df):
    """Store cleaned data in SQLite database"""
    engine = create_engine("sqlite:///data/bangladesh_development.db")
    
    # Write to database - replace if exists
    df.to_sql(
        "development_indicators", 
        engine, 
        if_exists="replace", 
        index=False
    )
    
    print(f"\nStored {len(df)} rows in SQLite database")
    print("Table: development_indicators")
    
    # Verify by reading back
    verification = pd.read_sql(
        "SELECT year, GDP_current_USD, literacy_rate FROM development_indicators ORDER BY year DESC LIMIT 5", 
        engine
    )
    print("\nMost recent 5 years:")
    print(verification)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = load_and_clean()
    df.to_csv("data/clean_data.csv", index=False)
    store_to_database(df)