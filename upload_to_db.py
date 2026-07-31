import os

import pandas as pd
from sqlalchemy import create_engine

DB_URL = os.environ.get("DB_URL")
if not DB_URL:
    raise SystemExit(
        "Variable d'environnement DB_URL manquante. "
        "Exemple : set DB_URL=postgresql://user:pass@host/db?sslmode=require"
    )

print("Chargement du CSV...")
df = pd.read_csv("donnees_aqi.csv")
print(f"  Lignes: {len(df)}")
print(f"  Colonnes: {list(df.columns)}")

print("Connexion a PostgreSQL...")
engine = create_engine(DB_URL)

with engine.begin() as conn:
    conn.exec_driver_sql("DROP TABLE IF EXISTS fact_aqi CASCADE;")
    print("  Table existante supprimee")

print("Creation de la table et insertion...")
df.to_sql("fact_aqi", engine, if_exists="replace", index=False, method="multi", chunksize=1000)
print(f"  {len(df)} lignes inserees dans fact_aqi")

with engine.connect() as conn:
    count = conn.exec_driver_sql("SELECT COUNT(*) FROM fact_aqi").scalar()
    print(f"  Verification: {count} lignes dans la base")

print("Termine!")
