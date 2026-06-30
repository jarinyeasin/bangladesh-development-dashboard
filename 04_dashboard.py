"""
04_dashboard.py
---------------
Phase 4: Interactive Streamlit dashboard.

Reads:  data/bangladesh_development.db   (created by 02_clean_store.py)
        outputs/fig*.png                 (created by 03_visualize.py)

HOW TO RUN:
    streamlit run 04_dashboard.py

This opens a browser tab automatically at http://localhost:8501
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
from sqlalchemy import create_engine, text

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bangladesh Development Dashboard",
    page_icon="🇧🇩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── data loading ──────────────────────────────────────────────────────────────
DB_PATH = "data/bangladesh_development.db"


@st.cache_data
def load_data():
    """Load from SQLite. Cached so it only runs once per session."""
    if not os.path.exists(DB_PATH):
        st.error(
            f"Database not found at '{DB_PATH}'. "
            "Please run 02_clean_store.py first."
        )
        st.stop()

    engine = create_engine(f"sqlite:///{DB_PATH}")
    with engine.connect() as conn:
        df = pd.read_sql(
            text("SELECT * FROM development_indicators ORDER BY year"),
            conn,
        )
    return df


df = load_data()

# ── sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/f/f9/Flag_of_Bangladesh.svg",
    width=120,
)
st.sidebar.title("🇧🇩 Bangladesh\nDevelopment Dashboard")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Data source:** [World Bank Open Data](https://data.worldbank.org/country/BD)"
)
st.sidebar.markdown("**Built with:** Python · SQLite · Streamlit · Plotly")
st.sidebar.markdown("---")
st.sidebar.markdown("*Part of the Bangladesh Development Data Pipeline portfolio project.*")

# ── header ────────────────────────────────────────────────────────────────────
st.title("🇧🇩 Bangladesh Development Indicators")
st.markdown(
    "Economic and social development data sourced from the **World Bank Open Data API**. "
    "Use the explorer below to examine any indicator across any year range."
)
st.markdown("---")

# ── KPI metric cards ──────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

def latest_value(col_name):
    """Return the most recent non-null value for a column."""
    data = df.dropna(subset=[col_name])
    if data.empty:
        return None, None
    row = data.iloc[-1]
    return row[col_name], int(row["year"])

gdp, gdp_yr        = latest_value("GDP_billions")
lit, lit_yr        = latest_value("literacy_rate")
inet, inet_yr      = latest_value("internet_users_percent")
elec, elec_yr      = latest_value("electricity_access_percent")

with col1:
    if gdp is not None:
        st.metric(f"GDP ({gdp_yr})", f"${gdp:.1f}B")

with col2:
    if lit is not None:
        st.metric(f"Literacy Rate ({lit_yr})", f"{lit:.1f}%")

with col3:
    if inet is not None:
        st.metric(f"Internet Users ({inet_yr})", f"{inet:.1f}%")

with col4:
    if elec is not None:
        st.metric(f"Electricity Access ({elec_yr})", f"{elec:.1f}%")

st.markdown("---")

# ── interactive indicator explorer ───────────────────────────────────────────
st.subheader("📈 Explore Any Indicator Over Time")

INDICATOR_OPTIONS = {
    "GDP (USD Billions)":            "GDP_billions",
    "GDP Per Capita (USD)":          "GDP_per_capita_USD",
    "GDP Annual Growth (%)":         "GDP_growth_pct",
    "Literacy Rate (%)":             "literacy_rate",
    "Internet Users (%)":            "internet_users_percent",
    "Inflation Rate (%)":            "inflation_rate",
    "Unemployment Rate (%)":         "unemployment_rate",
    "Electricity Access (%)":        "electricity_access_percent",
    "Population (Millions)":         "total_population",
}

left, right = st.columns([1, 3])

with left:
    selected_label = st.selectbox("Select indicator:", list(INDICATOR_OPTIONS.keys()))
    selected_col   = INDICATOR_OPTIONS[selected_label]

    chart_type = st.radio("Chart type:", ["Line", "Bar", "Area"])

    data_for_slider = df.dropna(subset=[selected_col])
    if not data_for_slider.empty:
        min_yr = int(data_for_slider["year"].min())
        max_yr = int(data_for_slider["year"].max())
        year_range = st.slider("Year range:", min_yr, max_yr, (min_yr, max_yr))
    else:
        year_range = (1990, 2024)

with right:
    plot_data = df.dropna(subset=[selected_col])
    plot_data = plot_data[
        (plot_data["year"] >= year_range[0]) &
        (plot_data["year"] <= year_range[1])
    ]

    # Scale population to millions for readability
    y_col = selected_col
    if selected_col == "total_population":
        plot_data = plot_data.copy()
        plot_data["total_population"] = plot_data["total_population"] / 1e6

    if not plot_data.empty:
        title = f"{selected_label} — Bangladesh {year_range[0]}–{year_range[1]}"

        if chart_type == "Line":
            fig = px.line(plot_data, x="year", y=y_col, title=title, markers=True)
        elif chart_type == "Bar":
            fig = px.bar(plot_data, x="year", y=y_col, title=title)
        else:  # Area
            fig = px.area(plot_data, x="year", y=y_col, title=title)

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title=selected_label,
            hovermode="x unified",
            height=420,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected indicator and year range.")

st.markdown("---")

# ── static charts from Phase 3 ────────────────────────────────────────────────
st.subheader("📊 Overview Charts")

chart_files = {
    "GDP Trend":               "outputs/fig1_gdp_trend.png",
    "Development Indicators":  "outputs/fig2_development_indicators.png",
    "GDP Per Capita":          "outputs/fig3_gdp_per_capita.png",
    "Annual GDP Growth":       "outputs/fig4_gdp_growth.png",
    "Population Growth":       "outputs/fig5_population.png",
}

available = {k: v for k, v in chart_files.items() if os.path.exists(v)}

if available:
    tabs = st.tabs(list(available.keys()))
    for tab, (name, path) in zip(tabs, available.items()):
        with tab:
            st.image(path, use_container_width=True)
else:
    st.info("Run 03_visualize.py to generate the overview charts.")

st.markdown("---")

# ── raw data table ────────────────────────────────────────────────────────────
with st.expander("📋 View Raw Data Table"):
    display_cols = ["year"] + [
        c for c in df.columns
        if c not in ("year", "country") and not df[c].isna().all()
    ]
    st.dataframe(
        df[display_cols].sort_values("year", ascending=False),
        use_container_width=True,
        height=350,
    )
    csv = df[display_cols].to_csv(index=False)
    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="bangladesh_development_data.csv",
        mime="text/csv",
    )

# ── footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Data: World Bank Open Data (CC BY 4.0) · "
    "Built by Jarin Binta Yeasin · "
    "Portfolio project — Bangladesh Development Data Pipeline"
)
