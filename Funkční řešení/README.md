# MongoDB Cluster – Funkční řešení

Tento projekt implementuje distribuovaný MongoDB cluster s podporou shardingu, replikace a importu více datových sad. Obsahuje datovou analýzu v Pythonu, validační skripty a ukázkové MongoDB dotazy.


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

## 7. Použité datasety

DVM-Car: https://deepvisualmarketing.github.io/

Wolt Delivery DataSet: https://www.kaggle.com/datasets/muhammadwajeeharif/wolt-delivery-dataset



## Git LFS – správa velkých datových souborů

Tento projekt používá [Git LFS (Large File Storage)](https://git-lfs.github.com/) pro správu velkých CSV souborů.

### Instalace Git LFS

#### Linux / macOS
```bash
sudo apt install git-lfs
git lfs install

```

#### Windows (přes Chocolatey nebo oficiální instalátor)
```bash
choco install git-lfs
git lfs install
```

### Klonování projektu

```bash
git clone https://github.com/rampouch-martin/NoSQL.git
cd NoSQL
git lfs pull
```

### Přidání souborů do LFS

```bash
git lfs track "*.csv"
git add .gitattributes
git add Data/Original/velky_soubor.csv
git commit -m "Přidán velký CSV soubor přes LFS"
git push
```