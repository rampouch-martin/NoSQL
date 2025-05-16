#!/bin/bash

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

# === WAIT FOR SHARDS ===
echo "Čekám 5 sekund na ustálení replik..."
sleep 5

# === ROUTER ===
echo "Inicializace routeru..."
docker compose exec router01 sh -c "mongosh < /scripts/init-router.js"

# === WAIT FOR ROUTER ===
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