import requests
import pandas as pd
import json

# World Bank API base URL
BASE_URL = "https://api.worldbank.org/v2/country/BD/indicator"

# Indicators we want for Bangladesh
# BD = Bangladesh country code
INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP_current_USD",
    "NY.GDP.PCAP.CD": "GDP_per_capita_USD", 
    "FP.CPI.TOTL.ZG": "inflation_rate",
    "SE.ADT.LITR.ZS": "literacy_rate",
    "IT.NET.USER.ZS": "internet_users_percent",
    "SP.POP.TOTL": "total_population",
    "SL.UEM.TOTL.ZS": "unemployment_rate",
    "EG.ELC.ACCS.ZS": "electricity_access_percent"
}

def fetch_indicator(indicator_code, indicator_name):
    """Fetch data for one indicator from World Bank API"""
    url = f"{BASE_URL}/{indicator_code}"
    params = {
        "format": "json",
        "per_page": 100,  # get 100 years of data
        "mrv": 30         # most recent 30 values
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching {indicator_name}: {response.status_code}")
        return None
    
    data = response.json()
    
    # World Bank returns [metadata, data] - we want index 1
    if len(data) < 2 or data[1] is None:
        print(f"No data for {indicator_name}")
        return None
    
    records = []
    for entry in data[1]:
        if entry["value"] is not None:  # skip missing values
            records.append({
                "year": int(entry["date"]),
                "value": float(entry["value"]),
                "indicator": indicator_name,
                "country": "Bangladesh"
            })
    
    return pd.DataFrame(records)

def fetch_all_indicators():
    """Fetch all indicators and combine into one dataframe"""
    all_data = []
    
    for code, name in INDICATORS.items():
        print(f"Fetching {name}...")
        df = fetch_indicator(code, name)
        if df is not None:
            all_data.append(df)
    
    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values(["indicator", "year"])
    
    return combined

if __name__ == "__main__":
    df = fetch_all_indicators()
    import os
    os.makedirs("data", exist_ok=True)  # creates data/ folder if missing
    df.to_csv("data/raw_world_bank_data.csv", index=False)
    print(f"\nSaved {len(df)} records to data/raw_world_bank_data.csv")
    print(df.groupby("indicator")["year"].agg(["min", "max", "count"]))