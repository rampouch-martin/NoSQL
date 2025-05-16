import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://martin:rampouch@127.0.0.1:27117,127.0.0.1:27118/?authMechanism=DEFAULT")
db = client["RampaBase"]

df = pd.read_csv("Cleaned/wolt_data_cleaned.csv")
db.wolt_data.drop()
db.wolt_data.insert_many(df.to_dict(orient="records"))

print(f"Importováno: {db.woltData.count_documents({})} záznamů do kolekce 'wolt_data'")
