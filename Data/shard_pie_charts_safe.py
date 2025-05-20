
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import os

# Připojení k MongoDB
client = pymongo.MongoClient("mongodb://martin:rampouch@127.0.0.1:27117/?authMechanism=DEFAULT")
db = client["RampaBase"]
config_db = client["config"]

# Výstupní složka
os.makedirs("Statistiky", exist_ok=True)

# Získání všech shardovaných kolekcí v databázi RampaBase
collections_info = config_db.collections.find({"_id": {"$regex": "^RampaBase\."}})
collection_entries = list(collections_info)

# Zpracování všech kolekcí
for entry in collection_entries:
    ns = entry["_id"]
    collection_name = ns.split(".")[1]
    collection_uuid = entry["uuid"]

    # Chunky podle UUID
    chunks_pipeline = [
        {"$match": {"uuid": collection_uuid}},
        {"$group": {"_id": "$shard", "chunks": {"$sum": 1}}}
    ]
    chunks = list(config_db.chunks.aggregate(chunks_pipeline))
    if not chunks:
        print(f"Přeskakuji {collection_name} – žádné chunky.")
        continue
    chunks_df = pd.DataFrame(chunks).rename(columns={"_id": "shard"})

    # Počet dokumentů
    try:
        total_docs = db[collection_name].estimated_document_count()
    except Exception:
        total_docs = 0

    total_chunks = chunks_df["chunks"].sum()
    if total_chunks == 0 or total_docs == 0:
        print(f"Přeskakuji {collection_name} – žádná data.")
        continue

    chunks_df["collection"] = collection_name
    chunks_df["documents"] = (chunks_df["chunks"] / total_chunks * total_docs).round().astype(int)

    # Vykreslení koláče pokud má smysluplná data
    if chunks_df["documents"].sum() > 0 and not chunks_df["documents"].isnull().any():
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(chunks_df['documents'], labels=chunks_df['shard'], autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Distribuce dokumentů – {collection_name}")
        plt.tight_layout()
        plt.savefig(f"Statistiky/pie_{collection_name}.png")
        plt.close()
    else:
        print(f"Přeskakuji {collection_name} – graf bez smysluplných dat.")
