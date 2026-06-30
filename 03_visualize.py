import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/clean_data.csv")

# Set consistent style
plt.style.use("seaborn-v0_8-whitegrid")
COLORS = ["#2196F3", "#4CAF50", "#FF5722", "#9C27B0"]

# --- Figure 1: GDP over time ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["year"], df["GDP_current_USD"] / 1e9, 
        color=COLORS[0], linewidth=2.5, marker="o", markersize=4)
ax.set_title("Bangladesh GDP 1990–2024", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Year")
ax.set_ylabel("GDP (USD Billions)")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0fB"))
plt.tight_layout()
plt.savefig("outputs/fig1_gdp_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Figure 2: Development indicators dashboard ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Bangladesh Development Indicators", fontsize=16, fontweight="bold")

indicators = [
    ("literacy_rate", "Literacy Rate (%)", COLORS[0]),
    ("internet_users_percent", "Internet Users (%)", COLORS[1]),
    ("electricity_access_percent", "Electricity Access (%)", COLORS[2]),
    ("unemployment_rate", "Unemployment Rate (%)", COLORS[3])
]

for ax, (col, label, color) in zip(axes.flat, indicators):
    data = df.dropna(subset=[col])
    ax.plot(data["year"], data[col], color=color, linewidth=2, marker="o", markersize=3)
    ax.set_title(label, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("%")

plt.tight_layout()
plt.savefig("outputs/fig2_development_indicators.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Figure 3: GDP per capita ---
fig, ax = plt.subplots(figsize=(10, 5))
data = df.dropna(subset=["GDP_per_capita_USD"])
ax.fill_between(data["year"], data["GDP_per_capita_USD"], 
                alpha=0.3, color=COLORS[1])
ax.plot(data["year"], data["GDP_per_capita_USD"], 
        color=COLORS[1], linewidth=2.5)
ax.set_title("Bangladesh GDP Per Capita Growth", fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("USD Per Person")
plt.tight_layout()
plt.savefig("outputs/fig3_gdp_per_capita.png", dpi=150, bbox_inches="tight")
plt.close()

print("All figures saved to outputs/")