
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from math import radians, sin, cos, sqrt, atan2
import folium
from folium.plugins import HeatMap

DATASET_NAME = "Wolt"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "Original", DATASET_NAME + ".csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Statistika output", DATASET_NAME)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Načtení a základní úpravy
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()
df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
df["delivery_delay"] = df["ACTUAL_DELIVERY_MINUTES"] - df["ESTIMATED_DELIVERY_MINUTES"]

# Výpočet vzdálenosti pomocí Haversinovy rovnice
def haversine(row):
    R = 6371  # km
    lat1, lon1, lat2, lon2 = map(radians, [row["USER_LAT"], row["USER_LONG"], row["VENUE_LAT"], row["VENUE_LONG"]])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

df["distance_km"] = df.apply(haversine, axis=1)

# Výpočet počtu unikátních GPS pozic
unique_user_coords = df[["USER_LAT", "USER_LONG"]].dropna().drop_duplicates().shape[0]
total_coords = len(df)

# Výpis do souboru
log_path = os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_vystup.txt")
with open(log_path, "w", encoding="utf-8") as f:
    f.write(f"Počet záznamů: {len(df)}\n")
    f.write(f"Počet sloupců: {df.shape[1]}\n")
    f.write(f"Počet chybějících hodnot: {df.isnull().sum().sum()}\n")
    f.write(f"Průměrné zpoždění: {df['delivery_delay'].mean():.2f} min\n")
    f.write(f"Mediánové zpoždění: {df['delivery_delay'].median():.2f} min\n")
    f.write(f"Průměrná vzdálenost: {df['distance_km'].mean():.2f} km\n\n")
    f.write(f"Unikátních kombinací souřadnic uživatelů: {unique_user_coords} z {total_coords} záznamů\n")
    if unique_user_coords < total_coords * 0.1:
        f.write("Poznámka: Velmi nízký počet unikátních souřadnic naznačuje, že GPS data mohla být zaokrouhlena nebo agregována z důvodu anonymizace. Výsledná heatmapa proto může působit pravidelně.\n")


# Histogram zpoždění doručení
plt.figure(figsize=(10, 5))
sns.histplot(df["delivery_delay"], bins=50, kde=False, color="skyblue")
plt.title("Zpoždění doručení (v minutách)")
plt.xlabel("Zpoždění (minuty)")
plt.ylabel("Počet objednávek")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_delay_histogram.png"))

# scatter plot
plt.figure(figsize=(6, 6))
sns.scatterplot(x="USER_LONG", y="USER_LAT", data=df, alpha=0.05, edgecolor=None)
plt.title("Rozložení objednávek podle polohy zákazníků")
plt.xlabel("Zeměpisná délka")
plt.ylabel("Zeměpisná šířka")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_user_location_scatter.png"))

# Nově: folium heatmapa uživatelů
m = folium.Map(location=[df["USER_LAT"].mean(), df["USER_LONG"].mean()], zoom_start=13)
heat_data = df[["USER_LAT", "USER_LONG"]].dropna().values.tolist()
HeatMap(heat_data, radius=10, blur=15, max_zoom=1).add_to(m)
m.save(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_user_location_heatmap.html"))

# Korelace počasí vs. zpoždění
plt.figure(figsize=(8, 6))
sns.heatmap(df[["delivery_delay", "PRECIPITATION", "WIND_SPEED", "TEMPERATURE"]].corr(), annot=True, cmap="coolwarm")
plt.title("Korelace zpoždění a počasí")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_weather_correlation.png"))
