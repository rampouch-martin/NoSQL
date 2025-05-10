#!/bin/bash
echo "[INIT] Waiting 20s for MongoDB cluster to be ready..."
sleep 20

echo "[INIT] Initializing config servers..."
mongosh --host configsvr01:27017 /scripts/init-configserver.js

echo "[INIT] Initializing shards..."
mongosh --host shard01-a:27017 /scripts/init-shard01.js
mongosh --host shard02-a:27017 /scripts/init-shard02.js
mongosh --host shard03-a:27017 /scripts/init-shard03.js

echo "[INIT] Initializing router (wait 10s)..."
sleep 10
mongosh --host router01:27017 < /scripts/init-router.js

echo "[INIT] Setting up authentication..."
mongosh --host configsvr01:27017 /scripts/auth.js
mongosh --host shard01-a:27017 /scripts/auth.js
mongosh --host shard02-a:27017 /scripts/auth.js
mongosh --host shard03-a:27017 /scripts/auth.js

echo "[INIT] Cluster setup complete."
