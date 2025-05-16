# import pandas as pd
# from pymongo import MongoClient

# client = MongoClient("mongodb://martin:rampouch@127.0.0.1:27117,127.0.0.1:27118/?authMechanism=DEFAULT")
# db = client["RampaBase"]

# df = pd.read_csv("Cleaned/photos_cleaned.csv")
# db.photos.drop()
# db.photos.insert_many(df.to_dict(orient="records"))

# print(f"Importováno: {db.photos.count_documents({})} záznamů do kolekce 'photos'")


import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://martin:rampouch@127.0.0.1:27117,127.0.0.1:27118/?authMechanism=DEFAULT")
db = client["RampaBase"]

df = pd.read_csv("Cleaned/photos_cleaned.csv")

# Zamezit problémům s _id
if "_id" in df.columns:
    df = df.drop(columns=["_id"])

db.photos.drop()

# Dávkové vkládání
batch_size = 10000
total = len(df)
print(f"Importuji {total} záznamů po {batch_size} dávkách...")

for i in range(0, total, batch_size):
    batch = df.iloc[i:i+batch_size].to_dict(orient="records")
    db.photos.insert_many(batch)
    print(f"Záznamy {i} až {min(i+batch_size, total)} vloženy.")

print(f"Import hotov: {db.photos.count_documents({})} záznamů")
