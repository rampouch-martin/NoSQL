### Datasety - téma: Automotive


# vytvoř venv ve složce .venv
python3 -m venv .venv

# aktivuj ho
source .venv/bin/activate
deactivate

docker compose exec router01 mongosh -u martin -p rampouch --authenticationDatabase admin


MongoCompass
Connection string router01: mongodb://martin:rampouch@127.0.0.1:27117,127.0.0.1:27118/?authMechanism=DEFAULT


Zjištění rozdělení dat na shardech:
sh.getShardedDataDistribution()