# 🇧🇩 Bangladesh Development Data Pipeline

**Jarin Binta Yeasin** | Mass Communication & Journalism | University of Dhaka  
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas)](https://pandas.pydata.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![World Bank](https://img.shields.io/badge/Data-World%20Bank%20Open%20Data-009FDA)](https://data.worldbank.org)

> 🔗 **[View Live Dashboard](https://bangladesh-development-dashboard-mneydmy24fk5pew5drbtkt.streamlit.app/)**

---

## Overview

An automated end-to-end data engineering pipeline that fetches Bangladesh's economic and social development indicators from the **World Bank Open Data API**, stores them in a SQLite database, generates publication-quality visualizations, and serves an interactive Streamlit dashboard.

This project demonstrates the full data engineering lifecycle — API ingestion, ETL pipeline design, relational database storage, time-series visualization, and live deployment — applied to a socially meaningful dataset about Bangladesh's development trajectory over 30+ years.

---

## Key Indicators Tracked

| Indicator | World Bank Code |
|---|---|
| GDP (current USD) | NY.GDP.MKTP.CD |
| GDP Per Capita (USD) | NY.GDP.PCAP.CD |
| Inflation Rate (%) | FP.CPI.TOTL.ZG |
| Literacy Rate (%) | SE.ADT.LITR.ZS |
| Internet Users (%) | IT.NET.USER.ZS |
| Total Population | SP.POP.TOTL |
| Unemployment Rate (%) | SL.UEM.TOTL.ZS |
| Electricity Access (%) | EG.ELC.ACCS.ZS |

---

## Pipeline Architecture

```
World Bank API
     │
     ▼
01_fetch_data.py          ← REST API calls, long-format DataFrame
     │
     ▼
data/raw_world_bank_data.csv
     │
     ▼
02_clean_store.py         ← cleaning, pivot, derived columns, SQLite storage
     │
     ├─► data/clean_data.csv
     └─► data/bangladesh_development.db   (SQLite)
               │
               ├─► 03_visualize.py        ← 5 publication-quality PNG charts
               │         └─► outputs/fig*.png
               │
               └─► 04_dashboard.py        ← Interactive Streamlit dashboard
                         └─► http://localhost:8501
```

---

## Project Structure

```
bangladesh-development-dashboard/
│
├── 01_fetch_data.py         # Phase 1: World Bank API → CSV
├── 02_clean_store.py        # Phase 2: Clean → SQLite database
├── 03_visualize.py          # Phase 3: Generate PNG charts
├── 04_dashboard.py          # Phase 4: Streamlit dashboard
│
├── data/                    # Created automatically on first run
│   ├── raw_world_bank_data.csv
│   ├── clean_data.csv
│   └── bangladesh_development.db
│
├── outputs/                 # Created automatically on first run
│   ├── fig1_gdp_trend.png
│   ├── fig2_development_indicators.png
│   ├── fig3_gdp_per_capita.png
│   ├── fig4_gdp_growth.png
│   └── fig5_population.png
│
├── requirements.txt
└── README.md
```

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/jarinyeasin/bangladesh-development-dashboard.git
cd bangladesh-development-dashboard
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the pipeline in order
```bash
python 01_fetch_data.py      # fetch from World Bank API
python 02_clean_store.py     # clean + store in SQLite
python 03_visualize.py       # generate charts
streamlit run 04_dashboard.py  # launch dashboard
```

The dashboard opens automatically at **http://localhost:8501**

---

## Selected Findings

Bangladesh's development trajectory over 1990–2024 reveals several notable patterns:

- **GDP growth:** Bangladesh sustained one of the highest GDP growth rates in South Asia, growing from approximately $30B in 1990 to over $400B by the early 2020s — a 13× increase.
- **Digital inclusion:** Internet penetration rose from near-zero in 2000 to over 40% by 2023, reflecting the rapid expansion of mobile internet infrastructure.
- **Literacy:** Adult literacy rates improved from approximately 35% in 1990 to over 74% by the early 2020s, driven by sustained investment in primary education.
- **Sleep displacement finding:** Raw GDP/screentime is less explanatory than behavioral mediators — a pattern this project connects to the companion [media usage wellbeing study](https://github.com/jarinyeasin/media-usage-wellbeing-project).

---

## Technical Notes

- **No API key required.** The World Bank Open Data API is completely free and open.
- **Reproducible.** Run the 4 scripts in sequence on any machine with Python 3.10+.
- **Offline-capable.** Once the database is built, scripts 3 and 4 run without internet access.
- **SQLite chosen** over CSV for the storage layer to demonstrate relational database concepts (table creation, SQL queries, index-based retrieval) while keeping zero infrastructure overhead.

---

## Future Work

- Expand to comparative analysis: Bangladesh vs. comparable economies (Vietnam, Cambodia, Sri Lanka)
- Add anomaly detection on GDP growth rate time series
- Integrate into the Bangla Sentiment Analysis Engine pipeline to correlate economic events with social media sentiment patterns in Bangla text — the natural next step in this portfolio's research trajectory

---

## Data Source

World Bank Open Data · [data.worldbank.org](https://data.worldbank.org/country/BD) · CC BY 4.0 License

---

## Author

**Jarin Binta Yeasin** | Final-year undergraduate, Mass Communication & Journalism, University of Dhaka  
📧 jarinyeasin@gmail.com · 🔗 [LinkedIn](https://www.linkedin.com/in/jarin-binta-yeasin-b61b88278) · 🐙 [GitHub](https://github.com/jarinyeasin)
