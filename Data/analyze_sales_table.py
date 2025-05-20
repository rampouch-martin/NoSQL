
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATASET_NAME = "Sales_table"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "Original", DATASET_NAME + ".csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Statistika output", DATASET_NAME)
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

# Výpis základních informací
year_cols = [col for col in df.columns if col.isdigit()]

# Přepočty
df["total_sales"] = df[year_cols].sum(axis=1)
year_totals = df[year_cols].sum()
top_models = df.sort_values("total_sales", ascending=False).head(10)

# Výpis do .txt
log_path = os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_vystup.txt")
with open(log_path, "w", encoding="utf-8") as f:
    f.write(f"Počet záznamů (modelů): {len(df)}\n")
    f.write(f"Počet sloupců: {df.shape[1]}\n")
    f.write(f"Počet chybějících hodnot: {df.isnull().sum().sum()}\n\n")

    f.write("Sloupce (včetně let):\n")
    f.write(", ".join(df.columns) + "\n\n")

    f.write("Celkové roční prodeje (2001–2020):\n")
    for year in sorted(year_cols):
        f.write(f"{year}: {int(year_totals[year]):,} vozů\n")
    f.write("\n")

    f.write("Top 10 nejprodávanějších modelů celkem:\n")
    for _, row in top_models.iterrows():
        f.write(f"{row['Genmodel_ID']} – {int(row['total_sales']):,} vozů\n")
        
# Vývoj celkových prodejů po letech
year_cols = [col for col in df.columns if col.isdigit()]
year_totals = df[year_cols].sum()
year_totals = year_totals.sort_index()

plt.figure(figsize=(10, 5))
sns.lineplot(x=year_totals.index, y=year_totals.values, marker="o")
plt.title("Celkové roční prodeje všech modelů (2001–2020)")
plt.xlabel("Rok")
plt.ylabel("Počet prodaných vozů")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_sales_by_year.png"))

# Top 10 nejprodávanějších modelů celkově
df["total_sales"] = df[year_cols].sum(axis=1)
top_models = df.sort_values("total_sales", ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_models["total_sales"], y=top_models["Genmodel_ID"], palette="viridis")
plt.title("Top 10 nejprodávanějších modelů (2001–2020)")
plt.xlabel("Počet prodaných vozů")
plt.ylabel("Genmodel_ID")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_top_models_total_sales.png"))

# Heatmapa prodejů v čase
top_15 = df.sort_values("total_sales", ascending=False).head(15)
heat_data = top_15.set_index("Genmodel_ID")[year_cols]

plt.figure(figsize=(12, 6))
sns.heatmap(heat_data, cmap="YlGnBu", annot=False, fmt="d")
plt.title("Prodeje top 15 modelů v čase")
plt.xlabel("Rok")
plt.ylabel("Genmodel_ID")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_heatmap_top_models.png"))
