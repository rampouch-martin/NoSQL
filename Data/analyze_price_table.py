
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATASET_NAME = "Price_table"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "Original", DATASET_NAME + ".csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Statistika output", DATASET_NAME)
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

log_path = os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_vystup.txt")
with open(log_path, "w", encoding="utf-8") as f:
    f.write(f"Počet záznamů: {len(df)}\n")
    f.write(f"Počet sloupců: {df.shape[1]}\n")
    f.write(f"Počet chybějících hodnot: {df.isnull().sum().sum()}\n")
    f.write(f"Chybějící hodnoty dle sloupců:\n{df.isnull().sum()}\n\n")

    f.write("Popisná statistika sloupce 'Price':\n")
    f.write(df["Entry_price"].describe().to_string())
    f.write("\n\n")

    top_models = df.groupby("Genmodel_ID")["Entry_price"].mean().sort_values(ascending=False).head(10)
    f.write("Top 10 modelů podle průměrné ceny:\n")
    f.write(top_models.to_string())
    f.write("\n")

# # Histogram cen
plt.figure(figsize=(10, 5))
sns.histplot(df["Entry_price"].dropna(), bins=100, kde=False)
plt.title("Rozložení cen nových vozů (v GBP)")
plt.xlabel("Cena (£)")
plt.ylabel("Počet modelů")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_histogram_price.png"))

# Vývoj průměrné ceny v čase
plt.figure(figsize=(10, 5))
price_by_year = df.groupby("Year")["Entry_price"].mean()
sns.lineplot(x=price_by_year.index, y=price_by_year.values, marker="o")
plt.title("Průměrná cena nových vozů podle roku")
plt.xlabel("Rok")
plt.ylabel("Průměrná cena (£)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_average_price_by_year.png"))

# Top modely dle průměrné ceny
plt.figure(figsize=(10, 6))
top_models = df.groupby("Genmodel_ID")["Entry_price"].mean().sort_values(ascending=False).head(10)
sns.barplot(x=top_models.values, y=top_models.index, palette="mako")
plt.title("Top 10 modelů s nejvyšší průměrnou cenou")
plt.xlabel("Průměrná cena (£)")
plt.ylabel("Genmodel_ID")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_top_models_price.png"))
