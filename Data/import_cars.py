import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://martin:rampouch@127.0.0.1:27117,127.0.0.1:27118/?authMechanism=DEFAULT")
db = client["RampaBase"]

df = pd.read_csv("Cleaned/car_advertisements_cleaned.csv")
db.cars.drop()
db.cars.insert_many(df.to_dict(orient="records"))

print(f"Importováno: {db.cars.count_documents({})} záznamů do kolekce 'cars'")
