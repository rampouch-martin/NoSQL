#!/bin/bash

wait_for_mongo() {
  local host=$1
  local port=$2
  echo -n "⏳ Čekám na MongoDB $host:$port "
  until docker compose exec "$host" mongosh --quiet --eval "db.runCommand({ ping: 1 })" &> /dev/null; do
    echo -n "."
    sleep 2
  done
  echo " ✅"
}

echo "[INIT] Startuji inicializační proces MongoDB clusteru..."

# Čekání na primární nody
wait_for_mongo configsvr01 27017
wait_for_mongo shard01-a 27017
wait_for_mongo shard02-a 27017
wait_for_mongo shard03-a 27017
wait_for_mongo router01 27017

echo "[CONFIG] Inicializace config serveru..."
docker compose exec configsvr01 mongosh <<EOF
var config = {
  "_id": "rs-config-server",
  configsvr: true,
  version: 1,
  members: [
    { _id: 0, host: "configsvr01:27017", priority: 1 },
    { _id: 1, host: "configsvr02:27017", priority: 0.5 },
    { _id: 2, host: "configsvr03:27017", priority: 0.5 }
  ]
};
rs.initiate(config, { force: true });
EOF

echo "[SHARD01] Inicializace shard 01..."
docker compose exec shard01-a mongosh <<EOF
var config = {
  "_id": "rs-shard-01",
  version: 1,
  members: [
    { _id: 0, host: "shard01-a:27017", priority: 1 },
    { _id: 1, host: "shard01-b:27017", priority: 0.5 },
    { _id: 2, host: "shard01-c:27017", priority: 0.5 }
  ]
};
rs.initiate(config, { force: true });
EOF

echo "[SHARD02] Inicializace shard 02..."
docker compose exec shard02-a mongosh <<EOF
var config = {
  "_id": "rs-shard-02",
  version: 1,
  members: [
    { _id: 0, host: "shard02-a:27017", priority: 1 },
    { _id: 1, host: "shard02-b:27017", priority: 0.5 },
    { _id: 2, host: "shard02-c:27017", priority: 0.5 }
  ]
};
rs.initiate(config, { force: true });
EOF

echo "[SHARD03] Inicializace shard 03..."
docker compose exec shard03-a mongosh <<EOF
var config = {
  "_id": "rs-shard-03",
  version: 1,
  members: [
    { _id: 0, host: "shard03-a:27017", priority: 1 },
    { _id: 1, host: "shard03-b:27017", priority: 0.5 },
    { _id: 2, host: "shard03-c:27017", priority: 0.5 }
  ]
};
rs.initiate(config, { force: true });
EOF

echo "[WAIT] Čekám 10 sekund na ustálení replikací..."
sleep 10

echo "[ROUTER] Přidání shardů do routeru..."
docker compose exec router01 mongosh <<EOF
sh.addShard("rs-shard-01/shard01-a:27017,shard01-b:27017,shard01-c:27017");
sh.addShard("rs-shard-02/shard02-a:27017,shard02-b:27017,shard02-c:27017");
sh.addShard("rs-shard-03/shard03-a:27017,shard03-b:27017,shard03-c:27017");
EOF

echo "[AUTH] Vytváření admin uživatele..."
for NODE in configsvr01 shard01-a shard02-a shard03-a; do
  docker compose exec "$NODE" mongosh <<EOF
use admin;
db.createUser({
  user: "your_admin",
  pwd: "your_password",
  roles: [ { role: "root", db: "admin" } ]
});
EOF
done

echo "[✅ HOTOVO] MongoDB cluster je plně inicializovaný!"
