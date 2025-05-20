sh.enableSharding("RampaBase")
db = db.getSiblingDB("RampaBase")

// Kolekce: cars (Ad_table)
db.createCollection("cars", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["Adv_ID", "Genmodel_ID", "Maker"],
      properties: {
        Adv_ID: { bsonType: "string" },
        Genmodel_ID: { bsonType: "string" },
        Maker: { bsonType: "string" }
      }
    }
  }
})
db.cars.createIndex({ Adv_ID: "hashed" })
sh.shardCollection("RampaBase.cars", { Adv_ID: "hashed" })

// Kolekce: car_prices (Price_table)
db.createCollection("car_prices", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["Genmodel_ID", "Entry_price"],
      properties: {
        Genmodel_ID: { bsonType: "string" },
        Entry_price: { bsonType: "double" }
      }
    }
  }
})
db.car_prices.createIndex({ Genmodel_ID: "hashed" })
sh.shardCollection("RampaBase.car_prices", { Genmodel_ID: "hashed" })

// Kolekce: sales (Sales_table)
db.createCollection("sales", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["Genmodel_ID"],
      properties: {
        Genmodel_ID: { bsonType: "string" }
      }
    }
  }
})
db.sales.createIndex({ Genmodel_ID: "hashed" })
sh.shardCollection("RampaBase.sales", { Genmodel_ID: "hashed" })

// Kolekce: wolt_data (Wolt)
db.createCollection("wolt_data", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["TIMESTAMP", "USER_LAT", "USER_LONG"],
      properties: {
        TIMESTAMP: { bsonType: "string" },
        USER_LAT: { bsonType: "double" },
        USER_LONG: { bsonType: "double" }
      }
    }
  }
})
db.wolt_data.createIndex({ _id: "hashed" })
sh.shardCollection("RampaBase.wolt_data", { _id: "hashed" })

// Kolekce: photos (Image_table)
db.createCollection("photos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["Image_ID", "Genmodel_ID"],
      properties: {
        Image_ID: { bsonType: "string" },
        Genmodel_ID: { bsonType: "string" }
      }
    }
  }
})
db.photos.createIndex({ Image_ID: "hashed" })
sh.shardCollection("RampaBase.photos", { Image_ID: "hashed" })

db.settings.updateOne(
  { _id: "chunksize" },
  { $set: { value: 1 } },
  { upsert: true }
);
