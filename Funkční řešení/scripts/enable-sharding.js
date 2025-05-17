sh.enableSharding("RampaBase")

db = db.getSiblingDB("RampaBase")

// Kolekce: cars
db.cars.createIndex({ _id: "hashed" })
sh.shardCollection("RampaBase.cars", { _id: "hashed" })

// Kolekce: car_prices
db.car_prices.createIndex({ _id: "hashed" })
sh.shardCollection("RampaBase.car_prices", { _id: "hashed" })

// Kolekce: sales
db.sales.createIndex({ _id: "hashed" })
sh.shardCollection("RampaBase.sales", { _id: "hashed" })

// Kolekce: wolt_data
db.wolt_data.createIndex({ _id: "hashed" })
sh.shardCollection("RampaBase.wolt_data", { _id: "hashed" })

// Kolekce: photos
db.photos.createIndex({ _id: "hashed" })
sh.shardCollection("RampaBase.photos", { _id: "hashed" })
