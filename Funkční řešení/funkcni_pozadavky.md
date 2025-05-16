SEMESTRÁLNÍ PROJEKT – MONGODB CLUSTER

FUNKČNÍ POŽADAVKY

1. Plně funkční MongoDB sharded cluster
- Obsahuje:
  - 3 konfigurační servery (configsvr)
  - 1 router (mongos)
  - 3 shardy (každý jako replikovaný set se 3 uzly)

2. Automatizované spuštění pomocí Docker Compose
- Jeden příkaz `docker compose up` musí:
  - Spustit všechny kontejnery
  - Spustit inicializační skripty (init-config, init-shards, init-router, auth, sharding)
  - Provést nastavení uživatele, sharding klíče, autentizaci

3. Zabezpečení MongoDB clusteru
- Implementována:
  - Autentizace pomocí uživatele (např. martin)
  - Autorizace s rolí `root`
  - Keyfile mezi instancemi MongoDB pro bezpečnou komunikaci

4. Připojení přes MongoDB URI
- Přes mongosh nebo jiného klienta pomocí connection string:
  mongodb://martin:rampouch@router01:27017/?authSource=admin

5. Podpora shardingového rozdělení dat
- Aktivovaný sharding na databázi `RampaBase`
- Kolekce `MyCollection` rozdělená podle složeného klíče:
  { oemNumber: "hashed", zipCode: 1, supplierId: 1 }

6. Možnost výpadku uzlu bez ztráty dostupnosti
- Replikace v každém shardu (3 uzly) zajišťuje toleranci výpadku
- Testovaný scénář výpadku 1 uzlu bez přerušení dostupnosti

7. Podpora práce s daty
- Databáze obsahuje data importovaná ze 3 datasetů (jeden s >5000 záznamy)
- Možnost spouštění dotazů (insert, update, aggregate, lookup…)
- Připraveno pro testování pomocí mongosh nebo skriptů

8. Analýza dat v Pythonu
- K dispozici Jupyter notebook (nebo .py) pro:
  - Načtení všech datasetů
  - Základní deskriptivní statistiky
  - Grafická analýza (pandas, matplotlib/seaborn)

9. 30 netriviálních MongoDB dotazů
- Využívají:
  - aggregate, unwind, lookup, project, group, sort
  - Práci s embedded dokumenty, indexy, shardingem
- Každý dotaz má:
  - Přirozené zadání
  - MongoDB příkaz
  - Vysvětlení co dotaz dělá
