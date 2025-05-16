
#!/bin/bash

MARKER_FILE="/scripts/.init_done"

if [ -f "$MARKER_FILE" ]; then
  echo "Inicializace už proběhla – přeskočeno."
  exit 0
fi

echo "Čekám, až se MongoDB kontejnery plně spustí..."
sleep 15 

echo "Inicializace config serveru..."
mongosh --host configsvr01 --file /scripts/init-configserver.js

echo "Inicializace shardů..."
mongosh --host shard01-a --file /scripts/init-shard01.js
mongosh --host shard02-a --file /scripts/init-shard02.js
mongosh --host shard03-a --file /scripts/init-shard03.js

echo "Inicializace routeru..."
mongosh --host router01 --file /scripts/init-router.js

echo "Nastavení autentizace..."
mongosh --host configsvr01 --file /scripts/auth.js
mongosh --host shard01-a --file /scripts/auth.js
mongosh --host shard02-a --file /scripts/auth.js
mongosh --host shard03-a --file /scripts/auth.js

echo "Zapnutí shardingu..."
mongosh --host router01 --port 27017 -u "martin" --authenticationDatabase admin --password "rampouch" <<EOF
if (!db.getSiblingDB("config").databases.find(d => d._id === "RampaBase")) {
  sh.enableSharding("RampaBase");
  db.adminCommand({ shardCollection: "RampaBase.MyCollection", key: { oemNumber: "hashed", zipCode: 1, supplierId: 1 } });
} else {
  print("Sharding pro databázi RampaBase už je aktivní.");
}
EOF

touch "$MARKER_FILE"
echo "Inicializace hotová!"

