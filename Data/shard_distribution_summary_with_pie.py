
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Shromáždíme výsledky pro všechny kolekce
all_data = []

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
        continue
    chunks_df = pd.DataFrame(chunks).rename(columns={"_id": "shard"})

    # Počet dokumentů v kolekci
    try:
        total_docs = db[collection_name].estimated_document_count()
    except Exception:
        total_docs = 0

    total_chunks = chunks_df["chunks"].sum()
    chunks_df["collection"] = collection_name
    chunks_df["documents"] = (chunks_df["chunks"] / total_chunks * total_docs).round().astype(int)

    all_data.append(chunks_df)

# Spojíme vše do jednoho DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Vykreslíme jeden společný graf: stacked bar plot podle kolekcí
plt.figure(figsize=(12, 7))
sns.barplot(data=final_df, x="collection", y="documents", hue="shard")
plt.title("Odhadovaný počet dokumentů na shardech pro kolekce v RampaBase")
plt.ylabel("Počet dokumentů (odhad)")
plt.xlabel("Kolekce")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("Statistiky/shard_summary_all_collections.png")
plt.show()

# === Vykreslení koláčových grafů pro každou kolekci ===
for collection in final_df['collection'].unique():
    subset = final_df[final_df['collection'] == collection]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(subset['documents'], labels=subset['shard'], autopct='%1.1f%%', startangle=90)
    ax.set_title(f"Distribuce dokumentů v kolekci '{collection}'")
    plt.tight_layout()
    plt.savefig(f"Statistiky/pie_{collection}.png")
    plt.close()
