# 🇧🇩 Bangladesh Development Data Pipeline

**Jarin Binta Yeasin** | Mass Communication & Journalism | University of Dhaka  
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas)](https://pandas.pydata.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![World Bank](https://img.shields.io/badge/Data-World%20Bank%20Open%20Data-009FDA)](https://data.worldbank.org)

> 🔗 **[View Live Dashboard](https://bangladesh-development-dashboard-mneydmy24fk5pew5drbtkt.streamlit.app/)**

---

## Research Motivation

Bangladesh presents one of the most analytically compelling development stories of the past three decades, a country that has sustained GDP growth rates averaging 6–7% annually while simultaneously navigating acute structural challenges: a population of 174 million in one of the world's most densely settled territories, persistent digital inequality between urban and rural areas, and an economy structurally exposed to climate risk through its low-lying delta geography.

Standard economic reporting on Bangladesh tends toward either uncritical optimism ("the Bengal Tiger economy") or crisis framing around political instability and climate vulnerability. Neither framing is analytically adequate. This project takes a different approach: letting longitudinal World Bank data speak across eight development dimensions simultaneously, making visible the relationships and the tensions that single-indicator reporting obscures.

Three research questions motivate the indicator selection:

1. **Does Bangladesh's aggregate GDP growth translate into proportional gains in human development indicators** literacy, electricity access, employment or does growth remain structurally concentrated?
2. **How did the COVID-19 shock of 2020 propagate across economic and social indicators**, and what does the recovery trajectory reveal about the resilience of Bangladesh's development model?
3. **Is digital inclusion (internet penetration) tracking with or lagging behind economic growth**, and what does the gap suggest about the distributional reach of the country's "Digital Bangladesh" agenda?

---

## Key Indicators & Analytical Rationale

| Indicator | World Bank Code | Why Included |
|---|---|---|
| GDP (current USD) | NY.GDP.MKTP.CD | Primary economic output measure; baseline for all relative comparisons |
| GDP Per Capita (USD) | NY.GDP.PCAP.CD | Distributional proxy — divergence from total GDP signals concentration |
| Inflation Rate (%) | FP.CPI.TOTL.ZG | Structural economic health; COVID-era spike is analytically significant |
| Literacy Rate (%) | SE.ADT.LITR.ZS | Human capital formation; lagging indicator of long-run development investment |
| Internet Users (%) | IT.NET.USER.ZS | Digital inclusion proxy; tested against GDP growth for co-movement |
| Total Population | SP.POP.TOTL | Denominator for per-capita metrics; context for unemployment interpretation |
| Unemployment Rate (%) | SL.UEM.TOTL.ZS | Labour market resilience; COVID shock visibility |
| Electricity Access (%) | EG.ELC.ACCS.ZS | Infrastructure floor for both digital inclusion and economic participation |

---

## Selected Findings

### 1. GDP Growth Without Proportional Employment Absorption

Bangladesh's GDP grew from approximately $30B in 1990 to over $400B by 2024, a 13× increase over three decades, placing it among the fastest-growing economies in South Asia. Yet the unemployment rate across the same period remained relatively stable in the 4–5% band, rather than declining as classical development theory would predict. Interpreted alongside population growth from roughly 108 million (1990) to 174 million (2024), this stability is not comforting, it suggests the economy is absorbing a rapidly expanding labour force without generating proportionally more formal employment. The informal sector, not captured in these ILO-modelled estimates, likely explains much of this divergence.

### 2. The COVID-19 Unemployment Signal and Recovery

The 2020 COVID-19 shock is visible in the data as a clear unemployment spike, the rate reached approximately 5.3% in 2020, its highest point in the observed period, rising from 4.22% in 2019. The spike was driven primarily by suspension of non-critical services, particularly hospitality, with partial recovery beginning as early as mid-2020 as informal sector activity resumed. By 2022–2023, the rate had returned to its pre-COVID band. The recovery is real but its speed reflects the informality of Bangladesh's employment structure as much as it reflects resilience: workers re-entered informal arrangements, not formal employment recovery.

### 3. Digital Inclusion: Rapid Growth, Persistent Structural Gap

Internet penetration in Bangladesh rose from near-zero in 2000 to approximately 40–47% by 2023–2025, driven almost entirely by mobile internet expansion following 4G rollout in 2018. The digital economy contributed an estimated 4.2% of GDP by 2025, exceeding earlier projections. However, the aggregate penetration figure conceals a significant urban-rural divide: urban penetration reached approximately 78% by 2025, while rural penetration lagged at 49%. Electricity access which reached approximately 88% nationally by the early 2020s functions as the infrastructural floor beneath digital inclusion; the remaining 12% without electricity access represents a population structurally excluded from digital participation regardless of mobile network availability.

### 4. The Literacy-Growth Relationship

Adult literacy improved from approximately 35% in 1990 to over 74% by the early 2020s, a 40-percentage-point gain over three decades. The trajectory tracks closely with GDP per capita growth, suggesting genuine co-movement rather than the literacy gains lagging growth (as occurs in economies where growth is primarily resource-extraction driven). This co-movement is consistent with Bangladesh's growth model, which is human-capital intensive through the garment sector and remittance economy, both of which reward basic literacy and numeracy.

---

## Pipeline Architecture

```
World Bank Open Data API
         │
         ▼
01_fetch_data.py          ← REST API calls, long-format DataFrame
         │
         ▼
data/raw_world_bank_data.csv
         │
         ▼
02_clean_store.py         ← cleaning, pivot to wide format,
         │                   derived columns, SQLite storage
         ├─► data/clean_data.csv
         └─► data/bangladesh_development.db   (SQLite)
                   │
                   ├─► 03_visualize.py        ← 5 publication-quality PNG charts
                   │         └─► outputs/fig*.png
                   │
                   └─► 04_dashboard.py        ← Interactive Streamlit dashboard
                             └─► live at Streamlit Cloud
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

### 2. Create a virtual environment
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
python 01_fetch_data.py        # fetch from World Bank API
python 02_clean_store.py       # clean + store in SQLite
python 03_visualize.py         # generate charts
streamlit run 04_dashboard.py  # launch dashboard at localhost:8501
```

---

## Technical Notes

- **No API key required.** The World Bank Open Data API is completely free and open.
- **Reproducible.** Run the 4 scripts in sequence on any machine with Python 3.10+.
- **Offline-capable.** Once the database is built, scripts 3 and 4 run without internet access.
- **SQLite chosen** over CSV for the storage layer to demonstrate relational database concepts — table creation, SQL queries, index-based retrieval, while keeping zero infrastructure overhead.
- **Streamlit Cloud deployment** uses direct API fetch with `@st.cache_data` to avoid local file dependency on the hosted environment.

---

## Limitations

- **ILO-modelled unemployment estimates** smooth over informal sector volatility, likely underestimating true COVID-era labour market disruption given Bangladesh's large informal economy.
- **Sample resolution** is annual. Quarterly or monthly data would reveal shock propagation and recovery dynamics more precisely, particularly around the 2020 COVID period.
- **Electricity access figures** are self-reported national estimates and may overstate rural access quality (connection vs. reliable supply).
- **Internet penetration** counts unique SIM connections rather than individual users, potentially double-counting in a market with high multi-SIM usage.

---

## Data Source

World Bank Open Data · [data.worldbank.org/country/BD](https://data.worldbank.org/country/BD) · CC BY 4.0 License

---

## Author

**Jarin Binta Yeasin** | Final-year undergraduate, Mass Communication & Journalism, University of Dhaka  
📧 jarinyeasin@gmail.com · 🔗 [LinkedIn](www.linkedin.com/in/jarin-binta-yeasin-b61b88278) · 🐙 [GitHub](https://github.com/jarinyeasin)
