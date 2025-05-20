import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
original_dir = BASE_DIR / "Data" / "Original"
cleaned_dir = BASE_DIR / "Data" / "Cleaned"
cleaned_dir.mkdir(parents=True, exist_ok=True)

def clean_car_advertisements():
    file_path = original_dir / "Ad_table (extra).csv"
    df = pd.read_csv(file_path)

    # Odstranit mezery v názvech sloupců
    df.columns = df.columns.str.strip()

    # Deduplikace podle Adv_ID
    if "Adv_ID" in df.columns:
        df = df.drop_duplicates(subset="Adv_ID", keep="first")

    output_path = cleaned_dir / "car_advertisements_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"Uloženo: {len(df)} záznamů do {output_path.name}")

def clean_prices():
    file_path = original_dir / "Price_table.csv"
    df = pd.read_csv(file_path)

    df = df.drop_duplicates()

    output_path = cleaned_dir / "car_prices_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"Uloženo: {len(df)} záznamů do {output_path.name}")

def clean_photos():
    file_path = original_dir / "Image_table.csv"
    df = pd.read_csv(file_path)

    # Deduplikace podle Image_ID (pokud existuje)
    if "Image_ID" in df.columns:
        df = df.drop_duplicates(subset="Image_ID", keep="first")

    output_path = cleaned_dir / "photos_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"Uloženo: {len(df)} záznamů do {output_path.name}")

def clean_sales():
    file_path = original_dir / "Sales_table.csv"
    df = pd.read_csv(file_path)

    year_cols = [col for col in df.columns if col.isdigit()]
    static_cols = ["Maker", "Genmodel", "Genmodel_ID"]

    cleaned_data = []

    for _, row in df.iterrows():
        sales_data = {year: int(row[year]) for year in year_cols if row[year] > 0}
        row_data = {col: row[col] for col in static_cols}
        for year, value in sales_data.items():
            row_data[year] = value
        cleaned_data.append(row_data)

    cleaned_df = pd.DataFrame(cleaned_data)
    output_path = cleaned_dir / "sales_cleaned.csv"
    cleaned_df.to_csv(output_path, index=False)
    print(f"Uloženo: {len(cleaned_df)} záznamů do {output_path.name}")

def clean_wolt():
    file_path = original_dir / "Wolt.csv"
    df = pd.read_csv(file_path)

    # Odstranění zbytečného sloupce 'Unnamed: 0'
    if "Unnamed: 0" in df.columns: 
        df = df.drop(columns=["Unnamed: 0"])

    # Deduplikace podle kombinace USER_LAT + USER_LONG + TIMESTAMP (přibližné určení unikátní objednávky)
    if all(col in df.columns for col in ["USER_LAT", "USER_LONG", "TIMESTAMP"]):
        df = df.drop_duplicates(subset=["USER_LAT", "USER_LONG", "TIMESTAMP"], keep="first")

    output_path = cleaned_dir / "wolt_data_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"Uloženo: {len(df)} záznamů do {output_path.name}")

# Spuštění všech čisticích funkcí
clean_car_advertisements()
clean_prices()
clean_photos()
clean_sales()
clean_wolt()

print("Všechna data byla očištěna.")
