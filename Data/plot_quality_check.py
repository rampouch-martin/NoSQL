
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATASET_NAME = "Image_table"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "Original", DATASET_NAME + ".csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Statistika output", DATASET_NAME)

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

# Barplot pro Quality_check
plt.figure(figsize=(8, 5))
df["Quality_check_filled"] = df["Quality_check"].fillna("NaN")
sns.countplot(x="Quality_check_filled", data=df, order=["P", "N", "NaN"], palette="pastel")
plt.title("Rozložení hodnot Quality_check")
plt.xlabel("Stav kontroly kvality")
plt.ylabel("Počet obrázků")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.figtext(0.5, -0.12, "P = prošlo kontrolou, N = neprošlo, NaN = nebylo kontrolováno", wrap=True, horizontalalignment='center', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_quality_check_barplot.png"), bbox_inches="tight")
