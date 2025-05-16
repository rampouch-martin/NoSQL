#!/bin/bash

echo "Čekám, až se MongoDB kontejnery plně spustí..."
sleep 15 

echo "Inicializace config serveru..."
docker compose exec configsvr01 bash "/scripts/init-configserver.js"

echo "Inicializace shardů..."
docker compose exec shard01-a bash "/scripts/init-shard01.js"
docker compose exec shard02-a bash "/scripts/init-shard02.js"
docker compose exec shard03-a bash "/scripts/init-shard03.js"

echo "Inicializace routeru..."
docker compose exec router01 sh -c "mongosh < /scripts/init-router.js"

echo "Nastavení autentizace..."
docker compose exec configsvr01 bash "/scripts/auth.js"
docker compose exec shard01-a bash "/scripts/auth.js"
docker compose exec shard02-a bash "/scripts/auth.js"
docker compose exec shard03-a bash "/scripts/auth.js"

echo "Přihlášení do routeru a zapnutí shardingu..."
docker compose exec router01 mongosh --port 27017 -u "martin" --authenticationDatabase admin --password "rampouch" <<EOF
sh.enableSharding("RampaBase")
db.adminCommand({ shardCollection: "RampaBase.MyCollection", key: { oemNumber: "hashed", zipCode: 1, supplierId: 1 } })
EOF

echo "Hotovo!"


