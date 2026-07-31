# Guide de création du Dashboard AQI — Power BI Desktop

## Prérequis
- **Power BI Desktop** (gratuit — [powerbi.microsoft.com](https://powerbi.microsoft.com))
- **Base PostgreSQL (Neon)** : `neondb` — table `fact_aqi` (42 398 lignes, 58 villes, 32 pays)
- Alternativement : le fichier `donnees_aqi.csv` si la base est indisponible

---

## Étape 1 : Se connecter au Data Warehouse (PostgreSQL)

1. Ouvrir **Power BI Desktop**
2. `Accueil` → `Obtenir des données` → `PostgreSQL`
3. Saisir :
   - **Serveur** : `ep-cold-wave-axo1eq9a-pooler.c-4.us-east-2.aws.neon.tech`
   - **Base de données** : `neondb`
   - **Mode** : *Importer* (volumes < 1M lignes)
4. Cliquer `OK` → saisir utilisateur `neondb_owner` + mot de passe
5. Dans l'aperçu, sélectionner la table **`fact_aqi`** → `Charger`

**Alternative (sans base) :** `Obtenir des données` → `Texte/CSV` → `donnees_aqi.csv` (séparateur virgule, encodage UTF-8).

**Résultat :** une table `fact_aqi` apparaît dans le volet **Champs**.

> ⚠️ Sécurité : ne pas afficher le mot de passe dans le rapport. Pour une présentation publique, utiliser le CSV ou un fichier `.pbix` sans credentials enregistrés.

---

## Étape 2 : Créer la table de dates (DAX)

`Modélisation` → `Nouvelle table` → Coller :

```dax
DimDate = 
VAR MinDate = MIN('fact_aqi'[date])
VAR MaxDate = MAX('fact_aqi'[date])
RETURN
ADDCOLUMNS(
    CALENDAR(MinDate, MaxDate),
    "year", YEAR([Date]),
    "month", MONTH([Date]),
    "month_name", FORMAT([Date], "MMMM"),
    "quarter", QUARTER([Date]),
    "day_of_week", WEEKDAY([Date], 2),
    "is_weekend", IF(WEEKDAY([Date], 2) >= 6, TRUE, FALSE),
    "year_month", YEAR([Date]) * 100 + MONTH([Date])
)
```

Puis :
- Cliquer droit sur `DimDate[Date]` → `Marquer comme table de dates`
- Créer la relation : `DimDate[Date]` ⟷ `fact_aqi[date]` (1 → plusieurs)

---

## Étape 3 : Créer les mesures DAX (6 KPIs)

`Modélisation` → `Nouvelle mesure` — créer ces 6 mesures :

```dax
AQI Moyen = ROUND(AVERAGE('fact_aqi'[aqi_value]), 1)

AQI Maximum = MAX('fact_aqi'[aqi_value])

AQI Minimum = MIN('fact_aqi'[aqi_value])

Total Mesures = COUNTROWS('fact_aqi')

Nb Villes = DISTINCTCOUNT('fact_aqi'[city_name])

Polluant Dominant = 
VAR pm25 = AVERAGE('fact_aqi'[pm25]) / 15
VAR pm10 = AVERAGE('fact_aqi'[pm10]) / 45
VAR no2  = AVERAGE('fact_aqi'[no2])  / 13
VAR so2  = AVERAGE('fact_aqi'[so2])  / 15
VAR co   = AVERAGE('fact_aqi'[co])   / 4
VAR o3   = AVERAGE('fact_aqi'[o3])   / 51
VAR maxi = MAXX({pm25, pm10, no2, so2, co, o3}, [Value])
RETURN
SWITCH(
    TRUE(),
    maxi = pm25, "PM2.5",
    maxi = pm10, "PM10",
    maxi = no2,  "NO₂",
    maxi = so2,  "SO₂",
    maxi = co,   "CO",
    "O₃"
)
```

> Le « Polluant dominant » est calculé en normalisant chaque polluant par son seuil santé OMS (µg/m³ quotidien). Le polluant ayant le ratio le plus élevé est dominant.

---

## Étape 4 : Créer la colonne calculée (couleurs)

```dax
Couleur AQI = 
SWITCH(
    TRUE(),
    'fact_aqi'[aqi_value] <= 50,  "#00E400",
    'fact_aqi'[aqi_value] <= 100, "#FFFF00",
    'fact_aqi'[aqi_value] <= 150, "#FF7E00",
    'fact_aqi'[aqi_value] <= 200, "#FF0000",
    'fact_aqi'[aqi_value] <= 300, "#8F3F97",
    "#7E0023"
)
```

---

## Étape 5 : Construire le dashboard (4 pages)

### Page 1 : Vue d'Ensemble

| Visuel | Type | Champs | Réglages |
|--------|------|--------|----------|
| Titre | Zone de texte | « Dashboard AQI — Qualité de l'Air » | Taille 28, gras, `#1B2A4A` |
| **AQI Moyen** | Carte (KPI) | `AQI Moyen` | Appel : « AQI Moyen » |
| **AQI Maximum** | Carte (KPI) | `AQI Maximum` | Appel : « AQI Max » |
| **AQI Minimum** | Carte (KPI) | `AQI Minimum` | Appel : « AQI Min » |
| **Total Mesures** | Carte (KPI) | `Total Mesures` | Appel : « Mesures » |
| **Nb Villes** | Carte (KPI) | `Nb Villes` | Appel : « Villes » |
| **Polluant Dominant** | Carte (KPI) | `Polluant Dominant` | Appel : « Polluant dominant » |
| **Carte géographique** | Carte Bing | Lat: `latitude`, Long: `longitude`, Taille: `AQI Moyen` | Couleur par catégorie |

**Formatage KPI :** fond dégradé selon la valeur (vert → rouge), police blanche sur fond foncé.

### Page 2 : Analyse Temporelle

| Visuel | Type | Axe X | Axe Y | Légende |
|--------|------|-------|-------|---------|
| **Évolution AQI** | Courbe | `DimDate[date]` | `AQI Moyen` | — |
| **Heatmap mensuelle** | Matrice | Lignes: `DimDate[year]`, Colonnes: `DimDate[month_name]` | `AQI Moyen` | — |
| **Répartition catégories** | Anneau | Légende: `aqi_category` | Valeurs: `Total Mesures` | — |

**Heatmap :** format conditionnel par dégradé (vert → jaune → orange → rouge), totaux actifs.

### Page 3 : Analyse par Ville

| Visuel | Axe Y | Axe X | Filtre |
|--------|-------|-------|--------|
| **AQI par ville** | `city_name` | `AQI Moyen` | Trier descendant |
| **Top 10 polluées** | `city_name` (Top N=10) | `AQI Moyen` | Filtre visuel Top N = 10 |
| **Classement complet** | Table : `city_name`, `country`, `AQI Moyen`, `aqi_category` | | |

### Page 4 : Polluants & Analyse

| Visuel | Type | Détails |
|--------|------|---------|
| **Comparaison polluants** | Barres | Axe X: polluants, Valeur: moyenne pm25, pm10, no2, so2, co, o3 |
| **Évolution des polluants** | Lignes multiples | Axe X: `date`, Lignes: pm25, pm10, no2, o3 |
| **Radar polluants** | Radar | 6 axes : PM2.5, PM10, NO₂, SO₂, CO, O₃ |
| **Zone d'analyse** | Zone de texte | Coller le contenu de `analyse.md` + `rapport_bloc2.md` |

---

## Étape 6 : Filtres interactifs (Slicers)

1. **Ville** → Slicer liste déroulante → `city_name`
2. **Pays** → Slicer liste déroulante → `country`
3. **Date** → Slicer plage de dates → `DimDate[date]`
4. **Catégorie AQI** → Slicer liste déroulante → `aqi_category`

**Synchronisation :** `Affichage` → `Synchroniser les slicers` → toutes les pages.

---

## Étape 7 : Thème et design

1. `Affichage` → `Thèmes` → thème sobre (ex : « City »)
2. Arrière-plan `#F5F5F5`, titres `#1B2A4A`, cartes KPI `#2C3E50`
3. Palette AQI : `#00E400, #FFFF00, #FF7E00, #FF0000, #8F3F97, #7E0023`

---

## Étape 8 : Vérifications finales (checklist)

- [ ] 6 cartes KPI visibles (moyen, max, min, total, villes, polluant dominant)
- [ ] AQI moyen par ville (bar chart)
- [ ] Évolution de l'AQI dans le temps (courbe)
- [ ] Top 10 des villes les plus polluées
- [ ] Répartition des catégories AQI (donut)
- [ ] Carte géographique des villes
- [ ] Comparaison des polluants (PM2.5, PM10, CO, NO₂, O₃, SO₂)
- [ ] 4 filtres interactifs synchronisés
- [ ] Analyse et recommandations présentes
- [ ] Axes et unités affichés sur les graphiques
- [ ] Export PDF OK (`Fichier` → `Exporter` → `PDF`)

---

## Étape 9 : Export

1. `Fichier` → `Exporter` → `PDF` (pour le jury)
2. `Fichier` → `Enregistrer sous` → `dashboard_aqi.pbix`

---

## Structure du .pbix

```
dashboard_aqi.pbix
├── Tables
│   ├── fact_aqi (42 398 lignes, PostgreSQL Neon)
│   └── DimDate (DAX, 731 jours)
├── Mesures (6 KPIs)
│   ├── AQI Moyen · AQI Maximum · AQI Minimum
│   ├── Total Mesures · Nb Villes · Polluant Dominant
├── Pages (4) : Vue d'Ensemble, Temporel, Villes, Polluants
└── Slicers (4 synchronisés) : Ville, Pays, Date, Catégorie
```

---

## Dépannage

| Problème | Solution |
|----------|----------|
| Connecteur PostgreSQL absent | Installer « Npgsql » : `Obtenir des données` → rechercher `PostgreSQL` ; sinon passer par le connecteur ODBC |
| Carte Bing vide | Vérifier que `latitude`/`longitude` sont au type Nombre Décimal |
| Slicers ne filtrent pas | Vérifier la relation `DimDate[date]` ⟷ `fact_aqi[date]` |
| Valeurs AQI en texte | Convertir en Nombre entier dans Power Query |
| La mesure Polluant Dominant renvoie O₃ par défaut | Normal : cas par défaut du SWITCH ; vérifier les colonnes pm25…o3 |
