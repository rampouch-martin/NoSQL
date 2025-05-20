import pandas as pd
import os

# Cesta ke složce s CSV (změň podle potřeby)
csv_dir = "Original"

# Pro každý CSV soubor ve složce
for file in os.listdir(csv_dir):
    if file.endswith(".csv"):
        path = os.path.join(csv_dir, file)
        print(f"{file}")
        try:
            df = pd.read_csv(path, nrows=1)
            print("Sloupce:", df.columns.tolist())
        except Exception as e:
            print(f"Chyba při čtení souboru: {e}")
        print("-" * 60)
