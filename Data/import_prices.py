import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://martin:rampouch@127.0.0.1:27117,127.0.0.1:27118/?authMechanism=DEFAULT")
db = client["RampaBase"]

df = pd.read_csv("Cleaned/car_prices_cleaned.csv")
db.car_prices.drop()
db.car_prices.insert_many(df.to_dict(orient="records"))

print(f"Importováno: {db.car_prices.count_documents({})} záznamů do kolekce 'car_prices'")
