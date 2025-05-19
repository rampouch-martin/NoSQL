
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATASET_NAME = "Ad_table (extra)"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "Original", DATASET_NAME + ".csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Statistika output/Ad_table (extra)")

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

log_path = os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_vystup.txt")
with open(log_path, "w", encoding="utf-8") as f:
    f.write(f"Počet záznamů: {len(df)}\n")
    f.write(f"Počet sloupců: {df.shape[1]}\n")
    f.write(f"Počet duplicitních Adv_ID: {df['Adv_ID'].duplicated().sum()}\n")
    f.write(f"Počet unikátních modelů (Genmodel): {df['Genmodel'].nunique()}\n")
    f.write(f"Počet různých výrobců (Maker): {df['Maker'].nunique()}\n")
    f.write(f"Počet chybějících hodnot (celkem): {df.isnull().sum().sum()}\n\n")

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    summary = df[numeric_columns].describe().T
    f.write("Statistický přehled číselných sloupců:\n")
    f.write(summary.to_string())
    f.write("\n\n")

    top_makers = df["Maker"].value_counts().head(10)
    f.write("Top 10 značek:\n")
    f.write(top_makers.to_string())
    f.write("\n")

# Heatmapa - vizualizace základní statistiky
plt.figure(figsize=(12, 8))
sns.heatmap(summary, annot=True, fmt=".1f", cmap="Blues", cbar=True)
plt.title("Statistický přehled číselných sloupců")
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_statistika_heatmapa.png"))

# Histogram cen (bez outlierů - 99. percentil)
max_price = df["Price"].quantile(0.99)
filtered_df = df[df["Price"] <= max_price]

plt.figure(figsize=(10, 5))
sns.histplot(filtered_df["Price"].dropna(), bins=100, kde=False)
plt.title("Rozložení cen vozidel (bez outlierů)")
plt.xlabel("Cena (£)")
plt.ylabel("Počet")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_histogram_cen.png"))

# Rozložení výrobců
plt.figure(figsize=(10, 5))
sns.barplot(x=top_makers.values, y=top_makers.index)
plt.title("Top 10 výrobců dle počtu inzerátů")
plt.xlabel("Počet inzerátů")
plt.ylabel("Značka")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_top_znacky.png"))
