import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import os

client = pymongo.MongoClient("mongodb://martin:rampouch@127.0.0.1:27117/?authMechanism=DEFAULT")
db = client["RampaBase"]
config_db = client["config"]

os.makedirs("Statistiky", exist_ok=True)

collection_entries = list(config_db.collections.find({"_id": {"$regex": "^RampaBase\\."}}))

for entry in collection_entries:
    ns = entry["_id"]
    collection_name = ns.split(".")[1]
    collection_uuid = entry.get("uuid")
    if not collection_uuid:
        continue

    chunks = list(config_db.chunks.aggregate([
        {"$match": {"uuid": collection_uuid}},
        {"$group": {"_id": "$shard", "chunks": {"$sum": 1}}}
    ]))
    if not chunks:
        continue

    chunks_df = pd.DataFrame(chunks).rename(columns={"_id": "shard"})

    try:
        total_docs = db[collection_name].estimated_document_count()
    except Exception:
        continue

    total_chunks = chunks_df["chunks"].sum()
    if total_chunks == 0 or total_docs == 0:
        continue

    chunks_df["documents"] = (chunks_df["chunks"] / total_chunks * total_docs).round().astype(int)

    if chunks_df["documents"].sum() > 0 and not chunks_df["documents"].isnull().any():
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(chunks_df['documents'], labels=chunks_df['shard'], autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Distribuce dokumentů – {collection_name}")
        plt.tight_layout()
        plt.savefig(f"Statistiky/pie_{collection_name}.png")
        plt.close()
