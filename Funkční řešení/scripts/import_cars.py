import pandas as pd
from pymongo import MongoClient, errors
import json
from myImportLib import clean_mongo_types
import os

client = MongoClient("mongodb://martin:rampouch@127.0.0.1:27117,127.0.0.1:27118/?authMechanism=DEFAULT")
db = client["RampaBase"]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "data", "car_advertisements_cleaned.csv")
df = pd.read_csv(DATA_PATH)

db.cars.delete_many({})

batch_size = 10000
total = len(df)
print(f"Importuji {total} záznamů po {batch_size} dávkách...")

errors_count = 0
error_log = []

for i in range(0, total, batch_size):
    batch = df.iloc[i:i+batch_size].to_dict(orient="records")
    try:
        db.cars.insert_many(batch, ordered=False)
    except errors.BulkWriteError as bwe:
        errors = bwe.details.get("writeErrors", [])
        errors_count += len(errors)
        for err in errors:
            error_doc = err.get("op", {})
            error_log.append(clean_mongo_types(error_doc))
    print(f"Záznamy {i} až {min(i+batch_size, total)} vloženy.")

if errors_count > 0:
    os.makedirs(os.path.join(SCRIPT_DIR, "import_errors"), exist_ok=True)
    with open(os.path.join(SCRIPT_DIR, "import_errors/cars_errors.json"), "w", encoding="utf-8") as f:
        json.dump(error_log, f, ensure_ascii=False, indent=2)
    print(f"Import hotov: {db.cars.count_documents({})} záznamů, chyb: {errors_count}")
    print("Chybové záznamy zapsány do cars_errors.json")
else:
    print(f"Import hotov: {db.cars.count_documents({})} záznamů, žádné chyby.")
