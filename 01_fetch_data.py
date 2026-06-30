"""
01_fetch_data.py
----------------
Phase 1: Fetch Bangladesh development indicators from the World Bank API.
No API key required - World Bank data is completely free and open.

Run this script first. It creates: data/raw_world_bank_data.csv
"""

import requests
import pandas as pd
import os

# World Bank API base URL
BASE_URL = "https://api.worldbank.org/v2/country/BD/indicator"

# Indicators we want for Bangladesh
# BD = Bangladesh ISO country code
# Keys are World Bank indicator codes, values are our friendly column names
INDICATORS = {
    "NY.GDP.MKTP.CD":  "GDP_current_USD",
    "NY.GDP.PCAP.CD":  "GDP_per_capita_USD",
    "FP.CPI.TOTL.ZG":  "inflation_rate",
    "SE.ADT.LITR.ZS":  "literacy_rate",
    "IT.NET.USER.ZS":  "internet_users_percent",
    "SP.POP.TOTL":     "total_population",
    "SL.UEM.TOTL.ZS":  "unemployment_rate",
    "EG.ELC.ACCS.ZS":  "electricity_access_percent",
}


def fetch_indicator(indicator_code, indicator_name):
    """
    Fetch data for one World Bank indicator for Bangladesh.
    Returns a DataFrame or None if the request fails.
    """
    url = f"{BASE_URL}/{indicator_code}"
    params = {
        "format":   "json",
        "per_page": 100,   # retrieve up to 100 data points
        "mrv":      30,    # most recent 30 values
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Could not fetch {indicator_name}: {e}")
        return None

    data = response.json()

    # World Bank API returns a list: [metadata_dict, data_list]
    if len(data) < 2 or data[1] is None:
        print(f"  [WARNING] No data returned for {indicator_name}")
        return None

    records = []
    for entry in data[1]:
        if entry["value"] is not None:          # skip years with missing values
            records.append({
                "year":      int(entry["date"]),
                "value":     float(entry["value"]),
                "indicator": indicator_name,
                "country":   "Bangladesh",
            })

    if not records:
        print(f"  [WARNING] All values were null for {indicator_name}")
        return None

    return pd.DataFrame(records)


def fetch_all_indicators():
    """
    Loop through all indicators, fetch each one, and combine into
    a single long-format DataFrame (year | indicator | value | country).
    """
    all_data = []

    for code, name in INDICATORS.items():
        print(f"  Fetching: {name} ...")
        df = fetch_indicator(code, name)
        if df is not None:
            all_data.append(df)
            print(f"    -> {len(df)} records retrieved")

    if not all_data:
        raise RuntimeError("No data was fetched. Check your internet connection.")

    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values(["indicator", "year"]).reset_index(drop=True)

    return combined


if __name__ == "__main__":
    print("=" * 55)
    print("  Bangladesh Development Dashboard — Phase 1")
    print("  Fetching data from World Bank Open Data API")
    print("=" * 55)

    # Create data/ folder if it does not exist yet
    os.makedirs("data", exist_ok=True)

    df = fetch_all_indicators()

    output_path = "data/raw_world_bank_data.csv"
    df.to_csv(output_path, index=False)

    print()
    print(f"Saved {len(df)} records to {output_path}")
    print()
    print("Records per indicator:")
    print(df.groupby("indicator")["year"].agg(["min", "max", "count"]).to_string())
    print()
    print("Phase 1 complete. Run 02_clean_store.py next.")
