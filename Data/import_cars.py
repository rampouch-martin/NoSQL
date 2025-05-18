import pandas as pd
from pymongo import MongoClient, errors
import json
from myImportLib import clean_mongo_types

client = MongoClient("mongodb://martin:rampouch@127.0.0.1:27117,127.0.0.1:27118/?authMechanism=DEFAULT")
db = client["RampaBase"]

df = pd.read_csv("Cleaned/car_advertisements_cleaned.csv")
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

with open("cars_errors.json", "w", encoding="utf-8") as f:
    json.dump(error_log, f, ensure_ascii=False, indent=2)

print(f"Import hotov: {db.cars.count_documents({})} záznamů, chyb: {errors_count}")
