#!/bin/bash

INIT_MARKER="/data/.cluster_initialized"

if [ -f "$INIT_MARKER" ]; then
  echo "Cluster už byl dříve inicializován – přeskočeno."
  exit 0
fi

echo "Spouštím inicializaci MongoDB clusteru poprvé..."
sleep 15

# === CONFIG SERVER ===
echo "Inicializace config serveru..."
mongosh --host configsvr01:27017 -f /scripts/init-configserver.js

# === SHARDS ===
echo "Inicializace shardů..."
mongosh --host shard01-a:27017 -f /scripts/init-shard01.js
mongosh --host shard02-a:27017 -f /scripts/init-shard02.js
mongosh --host shard03-a:27017 -f /scripts/init-shard03.js

# === WAITING FOR MONGOS ===
echo "Čekám, než bude router01 připraven..."
until mongosh --host router01:27017 --eval "db.runCommand({ ping: 1 })" > /dev/null 2>&1; do
  echo "→ router01 ještě není připraven, čekám 2s..."
  sleep 2
done

# === ROUTER ===
echo "Inicializace routeru (přidání shardů)..."
mongosh --host router01:27017 -f /scripts/init-router.js

echo "Čekám 3 sekundy na ustálení routeru..."
sleep 3

# === AUTENTIZACE ===
echo "Vytváření uživatele na všech uzlech..."
for srv in configsvr01 shard01-a shard02-a shard03-a; do
  echo "- $srv"
  mongosh --host ${srv}:27017 -f /scripts/auth.js
  sleep 2
done

# === ENABLE SHARDING ===
echo "Zapnutí shardingu pro RampaBase..."
mongosh --host router01:27017 -u "martin" -p "rampouch" --authenticationDatabase admin -f /scripts/enable-sharding.js

echo "Inicializace MongoDB clusteru dokončena."

# === OZNAČENÍ, ŽE UŽ BYLO INIT ===
touch "$INIT_MARKER"
