# Projet AQI — Analyse de la Qualité de l'Air

**Bloc 2 : Visualisation de données** (travail individuel)

Analyse et dashboard interactif de l'Air Quality Index (AQI) à partir du Data Warehouse PostgreSQL (Neon).

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://anahantonerrie-aqi-dashboard-app-kopcr4.streamlit.app)

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

🔗 **Version déployée** : [anahantonerrie-aqi-dashboard-app-kopcr4.streamlit.app](https://anahantonerrie-aqi-dashboard-app-kopcr4.streamlit.app)

En local :

```bash
streamlit run app.py
# → http://localhost:8501
```

Filtres : Ville, Pays, Date, Catégorie AQI. 4 onglets : Temporel, Villes, Polluants, Analyse.

---

## KPIs du dashboard

AQI moyen · AQI maximum · AQI minimum · Total des mesures · Nombre de villes · **Polluant dominant**

## Visualisations

Évolution AQI (courbe + heatmap) · AQI par ville · Top 10 polluées · Répartition des catégories · Carte géographique · Comparaison des polluants (PM2.5, PM10, NO₂, SO₂, CO, O₃)

---

## Licence

Projet universitaire — données simulées à des fins pédagogiques.

