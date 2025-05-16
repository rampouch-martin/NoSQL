import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://martin:rampouch@127.0.0.1:27117,127.0.0.1:27118/?authMechanism=DEFAULT")
db = client["RampaBase"]

df = pd.read_csv("Cleaned/sales_cleaned.csv")
year_columns = [col for col in df.columns if col.isdigit()]

documents = []
for _, row in df.iterrows():
    sales_data = {year: int(row[year]) for year in year_columns if row[year] > 0}
    doc = {
        "Maker": row["Maker"],
        "Genmodel": row["Genmodel"],
        "Genmodel_ID": row["Genmodel_ID"],
        "sales": sales_data
    }
    documents.append(doc)

db.sales.drop()
db.sales.insert_many(documents)

print(f"Importováno: {db.sales.count_documents({})} záznamů do kolekce 'sales'")
