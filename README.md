# Projet AQI — Analyse de la Qualité de l'Air

**Bloc 2 : Visualisation de données** (travail individuel)

Analyse et dashboard interactif de l'Air Quality Index (AQI) à partir du Data Warehouse PostgreSQL (Neon).

---

## Contenu du projet

| Fichier | Description |
|---|---|
| `requetes_sql.sql` | DDL + requêtes SQL optimisées |
| `guide_powerbi.md` | Guide de construction du dashboard Power BI |
| `rapport_bloc2.md` | Conformité exigences du sujet ↔ livrables |
| `analyse.md` | Analyse complète + recommandations |
| `app.py` | Dashboard Streamlit (bonus, exploration interactive) |
| `donnees_aqi.csv` | Jeu de données : 42 398 mesures, 58 villes, 32 pays |
| `upload_to_db.py` | Chargement CSV → PostgreSQL |

---

## Livrable officiel : Power BI Desktop

Power BI est l'outil retenu (liste autorisée du sujet).

1. Ouvrir **Power BI Desktop**
2. `Obtenir des données` → **PostgreSQL** → serveur Neon / base `neondb` / table `fact_aqi`
3. Suivre **`guide_powerbi.md`**
4. Exporter en PDF pour la présentation

## Dashboard Streamlit (bonus)

```bash
streamlit run app.py
# → http://localhost:8501
```
