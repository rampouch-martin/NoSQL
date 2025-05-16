sh.enableSharding("RampaBase");
db.adminCommand({
  shardCollection: "RampaBase.MyCollection",
  key: { oemNumber: "hashed", zipCode: 1, supplierId: 1 }
});
