#!/bin/sh

echo "Čekám, až se MongoDB kontejnery plně spustí..."
sleep 15

# === CONFIG SERVER ===
echo "Inicializace config serveru..."
docker compose exec configsvr01 bash   scripts/init-configserver.js

# === SHARDS ===
echo "Inicializace shardů..."
docker compose exec shard01-a bash scripts/init-shard01.js
docker compose exec shard02-a bash scripts/init-shard02.js
docker compose exec shard03-a bash scripts/init-shard03.js

# === WAITING FOR MONGOS ===
echo "Čekám, než bude router01 připraven..."
until docker compose exec router01 mongosh --host localhost:27017 --eval "db.runCommand({ ping: 1 })" > /dev/null 2>&1; do
  echo "→ router01 ještě není připraven, čekám 2s..."
  sleep 2
done

# === ROUTER ===
echo "Inicializace routeru (přidání shardů)..."
docker compose exec router01 mongosh --host localhost:27017 -f scripts/init-router.js
echo "Čekám 3 sekund na ustálení routeru..."
sleep 3

# === AUTENTIZACE ===
echo "Vytváření uživatele na všech uzlech..."

echo "- configsvr01"
docker compose exec configsvr01 bash "/scripts/auth.js"

sleep 3
echo "- shard01-a"
docker compose exec shard01-a bash "/scripts/auth.js"

sleep 3
echo "- shard02-a"
docker compose exec shard02-a bash "/scripts/auth.js"

sleep 3
echo "- shard03-a"
docker compose exec shard03-a bash "/scripts/auth.js"

sleep 3
# === ENABLE SHARDING ===
echo "Zapnutí shardingu pro RampaBase..."
docker compose exec router01 mongosh -u "martin" -p "rampouch" --authenticationDatabase admin /scripts/enable-sharding.js

echo "Inicializace MongoDB clusteru hotová!"


# === Import data ===
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/import_all.py"
# echo "Importuji data do databáze RampaBase..."
# python3 import_all.py

echo "Import dat do databáze RampaBase hotov!"
echo "Script manual-cluster-init.sh hotov!"