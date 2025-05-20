# Instalace MongoDB Clusteru

## 1. Spuštění Docker kontejnerů
Nejprve přejděte do adresáře `Funkční řešení` a spusťte Docker Compose:

```bash
docker compose up -d
```
Tento příkaz spustí všechny definované kontejnery na pozadí.

## 2. Windows: požadavky na WSL
Pokud používáte Windows, je nutné mít funkční WSL s distribucí **Ubuntu**. 
V Docker Desktop povolte integraci v části:

`Settings → Resources → WSL Integration → Enable integration with additional distros`

## 3. Instalace Pythonu a knihoven
Ve WSL nebo Linuxu nainstalujte Python 3:

```bash
sudo apt install python3 python3-pip -y
```
Nainstalujte následující knihovny:

```bash
pip3 install pymongo pandas matplotlib seaborn bson folium
```

## 4. Inicializace clusteru a import dat
Po spuštění kontejnerů a instalaci knihoven spusťte inicializační skript:

```bash
./scripts/manual-cluster-init.sh
```
Tento skript nastaví MongoDB cluster a provede import dat.

## 5. Připojení do MongoDB

### Konzolové připojení:
```bash
docker compose exec router01 mongosh -u martin -p rampouch
```

### Connection string (např. pro MongoDB Compass nebo aplikace):
```
mongodb://martin:rampouch@127.0.0.1:27117,127.0.0.1:27118/?authMechanism=DEFAULT
```

## 6. Struktura projektu
```
Data/                              # Vstupní data a analýza dat
├── Cleaned/                       # Očištěné CSV soubory
├── Original/                      # Originální stažené datasety
├── Statistika output/             # Výstup statistických python scriptů
├── analyze_*.py                   # Analýzy jednotlivých datasetů
├── clean_valid_data.py            # Předzpracování a očištění
Dotazy/                            # MongoDB dotazy podle kategorií
Funkční řešení/                    # Cluster + skripty + docker-compose
├── docker-compose.yml             # Hlavní docker soubor
├── mongodb-build/                 # Image s keyfile autentizací
├── scripts/                       # Inicializační a importní skripty
```