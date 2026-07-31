# Rapport de Conformité — Bloc 2 : Visualisation de données AQI

**Projet** : Analyse de la Qualité de l'Air (AQI)
**Bloc** : 2 — Visualisation de données (travail individuel)
**Outil officiel** : Power BI Desktop (outil autorisé par le sujet)
**Outil complémentaire** : Dashboard Streamlit + Plotly (exploration interactive)
**Source** : Data Warehouse PostgreSQL (Neon) — table `fact_aqi`

---

## 1. Connexion au Data Warehouse

| Exigence | Réalisation |
|---|---|
| Se connecter au data warehouse du Bloc 1 | ✅ Base **PostgreSQL (Neon)** connectée — serveur `ep-cold-wave-axo1eq9a-pooler...neon.tech`, base `neondb` |
| Vérification de l'intégrité | ✅ 42 398 mesures, 58 villes, 32 pays, période 2023-01-01 → 2024-12-31 |
| Fichier de secours | ✅ `donnees_aqi.csv` (même contenu) |

---

## 2. Extraction par requêtes SQL

| Exigence | Réalisation |
|---|---|
| Extraire les données utiles via SQL | ✅ `requetes_sql.sql` — 25 requêtes optimisées : KPIs, évolution temporelle, top villes, catégories, polluants, heatmap, carte, filtres |
| Optimisation | ✅ Index non-cluster sur `city_id`, `date_id`, `aqi_value`, `aqi_category` ; jointures en étoile ; filtres poussés au niveau SQL |

---

## 3. Structure du dashboard (Power BI — 4 pages)

| Page | Contenu | Exigence couverte |
|---|---|---|
| **1. Vue d'Ensemble** | 6 cartes KPI + carte géographique | KPIs + carte |
| **2. Analyse Temporelle** | Courbe d'évolution + heatmap mensuelle + donut catégories | Évolution + répartition |
| **3. Analyse par Ville** | Bar chart AQI par ville + Top 10 polluées + classement complet | Moyenne par ville + Top 10 |
| **4. Polluants & Analyse** | Comparaison des 6 polluants + évolution + radar + zone d'analyse | Polluants + analyse |

---

## 4. KPIs affichés

| KPI | Réalisation (Power BI) | Réalisation (Streamlit) |
|---|---|---|
| AQI moyen | ✅ Mesure DAX `AQI Moyen` | ✅ Carte KPI |
| AQI maximum | ✅ Mesure DAX `AQI Maximum` | ✅ Carte KPI |
| AQI minimum | ✅ Mesure DAX `AQI Minimum` | ✅ Carte KPI |
| Nombre total de mesures | ✅ Mesure DAX `Total Mesures` | ✅ Carte KPI |
| Nombre de villes analysées | ✅ Mesure DAX `Nb Villes` | ✅ Carte KPI |
| **Polluant dominant** | ✅ Mesure DAX `Polluant Dominant` | ✅ Carte KPI |

---

## 5. Visualisations exigées

| Exigence | Power BI | Streamlit |
|---|---|---|
| AQI moyen par ville | ✅ Bar chart | ✅ Bar chart (Top 20) |
| Évolution de l'AQI dans le temps | ✅ Courbe + heatmap | ✅ Courbe + heatmap |
| Top 10 des villes les plus polluées | ✅ Bar chart (Top N = 10) | ✅ Bar chart |
| Répartition des catégories AQI | ✅ Donut | ✅ Donut |
| Min / Max / Moyenne | ✅ 3 KPIs | ✅ 3 KPIs |
| Carte géographique | ✅ Carte Bing (lat/lon) | ✅ Scattergeo |
| Comparaison des polluants | ✅ Barres + lignes + radar | ✅ Barres + lignes + radar |

---

## 6. Filtres interactifs

| Filtre | Power BI | Streamlit |
|---|---|---|
| Ville | ✅ Slicer déroulant | ✅ multiselect |
| Pays | ✅ Slicer déroulant | ✅ multiselect |
| Date | ✅ Slicer plage de dates | ✅ date_input |
| Catégorie AQI | ✅ Slicer déroulant | ✅ multiselect |
| Synchronisation | ✅ Toutes les pages | ✅ Barre latérale globale |

---

## 7. Analyse répondant aux questions du sujet

| Question du sujet | Réponse |
|---|---|
| Quelles villes sont les plus polluées ? | Delhi (257), Lahore (230), Dhaka (202), Lucknow (197), Harbin (186) — l'Asie du Sud domine |
| Comment l'AQI évolue-t-il dans le temps ? | Cycle saisonnier marqué : pics hivernaux (nov-fév), amélioration pendant les pluies (juin-sept) |
| Quels polluants contribuent le plus ? | **PM2.5** (dominant, r ≈ 0,92 avec l'AQI), PM10, puis NO₂ ; O₃ augmente en été (photochimie) |
| Tendances / périodes critiques ? | Hiver = période critique (inversion thermique, chauffage, brûlage agricole) ; tendance globale stable ±3% |
| Recommandations ? | Réduire les PM2.5 (transports, industrie, chauffage) ; ZFE ; interdire le brûlage agricole ; transports propres ; alertes précoces ; végétalisation |

📄 Analyse complète : `analyse.md` + onglet « Analyse » des dashboards.

---

## 8. Respect des contraintes du sujet

| Contrainte | Réalisation |
|---|---|
| Couleurs cohérentes (vert → jaune → orange → rouge) | ✅ Palette EPA : `#00E400` → `#FFFF00` → `#FF7E00` → `#FF0000` → `#8F3F97` → `#7E0023` |
| Dashboard responsive et professionnel | ✅ Layout « wide », 4 pages, titres et zone d'analyse |
| Graphiques correctement nommés | ✅ Titres explicites sur chaque visuel |
| Axes et unités affichés | ✅ (µg/m³, ppb, ppm selon polluant ; date ; AQI) |
| Requêtes SQL optimisées | ✅ Index + jointures en étoile + filtres SQL |

---

## 9. Fichiers livrés

| Fichier | Rôle |
|---|---|
| `requetes_sql.sql` | Requêtes SQL d'extraction optimisées |
| `guide_powerbi.md` | Guide de construction du dashboard Power BI (connexion, DAX, visuels) |
| `rapport_bloc2.md` | Ce document de conformité |
| `analyse.md` | Analyse complète + recommandations |
| `app.py` | Dashboard Streamlit (exploration interactive, bonus) |
| `donnees_aqi.csv` | Jeu de données (secours / import Power BI) |
| `upload_to_db.py` | Script de chargement CSV → PostgreSQL |

---

*Document généré le 30 juillet 2026 — Projet AQI, Bloc 2 : Visualisation de données.*
