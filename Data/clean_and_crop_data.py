import pandas as pd
import os
from pathlib import Path

# Základní cesta (relativní ke skriptu)
BASE_DIR = Path(__file__).resolve().parent.parent
original_dir = BASE_DIR / "Data" / "Original"
cleaned_dir = BASE_DIR / "Data" / "Cleaned"
cleaned_dir.mkdir(parents=True, exist_ok=True)

# Nastavení limitu řádků
row_limit = 10000

def process_csv(file_name: str, subset_col: str, output_name: str):
    print(f"Čistím {file_name} ...")
    file_path = original_dir / file_name
    df = pd.read_csv(file_path)

    print("Sloupce v souboru:")
    print(df.columns.tolist())

    if subset_col not in df.columns:
        print(f"Upozornění: Sloupec '{subset_col}' nebyl nalezen, data nebudou deduplikována.")
    else:
        df = df.drop_duplicates(subset=subset_col, keep="first")

    # Odstranit sloupce s >50 % null hodnot
    threshold = len(df) * 0.5
    df = df.loc[:, df.isnull().sum() < threshold]

    df_clean = df.head(row_limit)
    output_path = cleaned_dir / output_name
    df_clean.to_csv(output_path, index=False)
    print(f"Uloženo: {len(df_clean)} záznamů do {output_path.name}\n")

# 1. CARS – používá sloupec 'Adv_ID' jako identifikátor
process_csv("Ad_table (extra).csv", "Adv_ID", "cars_cleaned.csv")

# 2. PRICES – používá sloupec 'Genmodel_ID' jako identifikátor
process_csv("Price_table.csv", "Genmodel_ID", "prices_cleaned.csv")

# 3. SALES – používá sloupec 'Genmodel_ID' jako identifikátor
process_csv("Sales_table.csv", "Genmodel_ID", "sales_cleaned.csv")

print("Všechna data byla očištěna a zmenšena.")



# import pandas as pd
# import os

# # Složky
# original_dir = "Original"
# cleaned_dir = "Cleaned"
# os.makedirs(cleaned_dir, exist_ok=True)

# # Nastavení limitu řádků pro výběr
# row_limit = 10000

# # === 1. CARS ===
# print("Čistím Ad_table (extra).csv ...")
# cars_path = os.path.join(original_dir, "Ad_table (extra).csv")
# cars_df = pd.read_csv(cars_path)

# # Odstranění duplicitních VIN
# cars_df = cars_df.drop_duplicates(subset="vin", keep="first")

# # Odstranění sloupců, které mají více než 50 % chybějících hodnot
# threshold = len(cars_df) * 0.5
# cars_df = cars_df.loc[:, cars_df.isnull().sum() < threshold]

# # Výběr prvních 10 000 záznamů
# cars_clean = cars_df.head(row_limit)
# cars_clean.to_csv(os.path.join(cleaned_dir, "cars_cleaned.csv"), index=False)
# print(f"Uloženo: {len(cars_clean)} záznamů do cars_cleaned.csv")

# # === 2. PRICES ===
# print("Čistím Price_table.csv ...")
# prices_path = os.path.join(original_dir, "Price_table.csv")
# prices_df = pd.read_csv(prices_path)

# prices_df = prices_df.drop_duplicates(subset="vin", keep="first")
# prices_df = prices_df.loc[:, prices_df.isnull().sum() < threshold]
# prices_clean = prices_df.head(row_limit)
# prices_clean.to_csv(os.path.join(cleaned_dir, "prices_cleaned.csv"), index=False)
# print(f"Uloženo: {len(prices_clean)} záznamů do prices_cleaned.csv")

# # === 3. SALES ===
# print("Čistím Sales_table.csv ...")
# sales_path = os.path.join(original_dir, "Sales_table.csv")
# sales_df = pd.read_csv(sales_path)

# sales_df = sales_df.drop_duplicates(subset="vin", keep="first")
# sales_df = sales_df.loc[:, sales_df.isnull().sum() < threshold]
# sales_clean = sales_df.head(row_limit)
# sales_clean.to_csv(os.path.join(cleaned_dir, "sales_cleaned.csv"), index=False)
# print(f"Uloženo: {len(sales_clean)} záznamů do sales_cleaned.csv")

# print("Všechna data byla očištěna a zmenšena.")
