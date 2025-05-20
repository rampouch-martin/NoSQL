
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

# Výstupní log
log_path = os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_vystup.txt")
with open(log_path, "w", encoding="utf-8") as f:
    f.write(f"Počet záznamů: {len(df)}\n")
    f.write(f"Počet sloupců: {df.shape[1]}\n")
    f.write(f"Počet chybějících hodnot (celkem): {df.isnull().sum().sum()}\n")
    f.write(f"Chybějící hodnoty dle sloupců:\n{df.isnull().sum()}\n\n")

    top_models = df["Genmodel_ID"].value_counts().head(10)
    f.write("Top 10 Genmodel_ID podle počtu obrázků:\n")
    f.write(top_models.to_string())
    f.write("\n")

    if "Quality_check" in df.columns:
        qc_dist = df["Quality_check"].value_counts(dropna=False)
        f.write("\nRozložení hodnot Quality_check:\n")
        f.write(qc_dist.to_string())
        f.write("\n")
        
plt.figure(figsize=(14, 7))
viewpoint_order = sorted(df["Predicted_viewpoint"].dropna().unique())
sns.countplot(x="Predicted_viewpoint", data=df, order=viewpoint_order, color="skyblue", edgecolor="black")

plt.title("Rozložení kategoriálních úhlů pohledu (Predicted_viewpoint)")
plt.xlabel("Kód viewpointu")
plt.ylabel("Počet obrázků")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Legenda
legend_text = (
    "Legenda úhlů:\n"
    "0 = předek, 45 = předek zleva, 90 = levý bok, 135 = zadek zleva, 180 = zadek,\n"
    "225 = zadek zprava, 270 = pravý bok, 315 = předek zprava, 360 = pohled shora"
)
plt.figtext(0.5, -0.12, legend_text, wrap=True, horizontalalignment='center', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_viewpoint_histogram_legend.png"), bbox_inches="tight")

# Barplot top Genmodel_ID
plt.figure(figsize=(10, 5))
sns.barplot(x=top_models.values, y=top_models.index)
plt.title("Top 10 modelů podle počtu obrázků")
plt.xlabel("Počet obrázků")
plt.ylabel("Genmodel_ID")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_top_models.png"))

# # Sloupcový graf pro Quality_check
plt.figure(figsize=(8, 5))
sns.countplot(x="Quality_check", data=df, order=["P", "N", None], palette="pastel")
plt.title("Rozložení hodnot Quality_check")
plt.xlabel("Stav kontroly kvality")
plt.ylabel("Počet obrázků")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.figtext(0.5, -0.12, "P = Passed (prošlo ruční kontrolou), N = Not passed (neprošlo), NaN = nebylo kontrolováno", wrap=True, horizontalalignment='center', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, f"{DATASET_NAME}quality_check_barplot.png"), bbox_inches="tight")