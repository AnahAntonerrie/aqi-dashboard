# Analyse du Dashboard Qualité de l'Air (AQI)

## Projet AQI — Bloc 2 : Visualisation de données
**Data Analyst** — Juillet 2026

---

## 1. Villes les plus polluées

L'analyse des données sur la période 2023-2024 révèle une hiérarchie claire des villes les plus touchées par la pollution atmosphérique :

| Rang | Ville | Pays | AQI Moyen | Catégorie |
|------|-------|------|-----------|-----------|
| 1 | **Delhi** | Inde | 257 | Very Unhealthy |
| 2 | **Lahore** | Pakistan | 230 | Very Unhealthy |
| 3 | **Dhaka** | Bangladesh | 202 | Very Unhealthy |
| 4 | **Lucknow** | Inde | 197 | Unhealthy |
| 5 | **Harbin** | Chine | 186 | Unhealthy |
| 6 | **Beijing** | Chine | 165 | Unhealthy |
| 7 | **Tehran** | Iran | 160 | Unhealthy |
| 8 | **Mumbai** | Inde | 142 | Unhealthy for Sensitive Groups |
| 9 | **Karachi** | Pakistan | 140 | Unhealthy for Sensitive Groups |
| 10 | **Kolkata** | Inde | 137 | Unhealthy for Sensitive Groups |

**Observation clé :** Les 10 villes les plus polluées sont toutes situées en Asie du Sud ou de l'Est. L'Inde domine le classement avec 5 villes dans le Top 10.

---

## 2. Tendances observées

### 2.1 Répartition globale des catégories AQI

| Catégorie | Pourcentage | Interprétation |
|-----------|-------------|----------------|
| Good | 22,2% | Air sain — minoritaire |
| Moderate | 38,7% | Qualité acceptable — majorité |
| Unhealthy for Sensitive Groups | 24,9% | Risque pour populations sensibles |
| Unhealthy | 8,8% | Risque sanitaire général |
| Very Unhealthy | 5,4% | Niveau dangereux |
| Hazardous | ~0,02% | Urgence sanitaire (épisodes rares) |

**Tendance :** Près de **77% des mesures** dépassent le seuil "Good", indiquant que la pollution de l'air est un problème généralisé dans les zones urbannes analysées.

### 2.2 Évolution temporelle

- **Cycle saisonnier marqué** : L'AQI augmente significativement en hiver (novembre-février), particulièrement dans les villes à climat tempéré et les zones de mousson asiatiques.
- **Pics hivernaux** : Les villes indiennes (Delhi, Lucknow) voient leur AQI grimper de 30 à 50 points en décembre-janvier à cause de l'inversion thermique et du chauffage résidentiel.
- **Amélioration estivale** : Les pluies de mousson (juin-septembre) réduisent temporairement les niveaux de particules en suspension.
- **Contraste Nord-Sud** : Les villes de l'hémisphère nord montrent des variations saisonnières plus prononcées que celles de l'hémisphère sud.

### 2.3 Tendances annuelles 2023 → 2024

Comparaison des AQI moyens entre 2023 et 2024 :
- **Stabilité globale** : Les niveaux moyens restent comparables entre les deux années (±3%).
- **Légère amélioration** dans certaines villes chinoises (Beijing : -5%).
- **Stagnation ou dégradation** dans les villes sud-asiatiques (Delhi, Dhaka).

---

## 3. Périodes critiques

### 3.1 Calendrier de la pollution

| Période | Niveau de risque | Causes principales |
|---------|-----------------|-------------------|
| **Novembre à Février** | 🔴 Très élevé | Inversion thermique, chauffage, brûlage agricole |
| **Mars à Mai** | 🟡 Modéré | Printemps, vents variables |
| **Juin à Septembre** | 🟢 Plus bas | Mousson, pluies lessivantes |
| **Octobre** | 🟠 Élevé | Transition, accumulation des polluants |

### 3.2 Mois les plus pollués (AQI moyen global)

1. **Janvier** — AQI moyen le plus élevé (pics hivernaux généralisés)
2. **Décembre** — Deuxième plus haut niveau
3. **Novembre** — Début de la saison de pollution intense
4. **Juillet** — Mois le plus propre en moyenne (pluies de mousson)

### 3.3 Épisodes extrêmes

Les 7 enregistrements classés "Hazardous" (AQI > 300) ont eu lieu exclusivement à Delhi et Lahore pendant les mois de décembre et janvier.

---

## 4. Principaux polluants

### 4.1 Classement par concentration moyenne

| Polluant | Concentration moyenne | Contribution à l'AQI | Source principale |
|----------|---------------------|---------------------|-------------------|
| **PM10** | 62,4 µg/m³ | Élevée | Poussières, construction, routes |
| **PM2.5** | 38,1 µg/m³ | Très élevée | Combustion, industrie, véhicules |
| **NO₂** | 16,3 ppb | Modérée | Trafic routier, centrales thermiques |
| **O₃** | 12,1 ppb | Modérée | Réactions photochimiques (été) |
| **SO₂** | 5,2 ppb | Faible | Centrales au charbon, industrie |
| **CO** | 0,8 ppm | Faible | Combustion incomplète, véhicules |

### 4.2 Corrélations identifiées

- **PM2.5 ↔ AQI** : Corrélation très forte (r ≈ 0,92) — les PM2.5 sont le principal indicateur de l'AQI dans ce jeu de données.
- **PM10 ↔ PM2.5** : Corrélation forte (r ≈ 0,85) — les particules fines et grossières partagent des sources communes.
- **AQI ↔ Température** : Corrélation négative modérée (r ≈ -0,45) — l'air froid emprisonne les polluants (inversion thermique).
- **O₃ ↔ Température** : Corrélation positive en été (r ≈ 0,6) — l'ozone se forme par photochimie sous l'effet de la chaleur.

### 4.3 Répartition par type de ville

- **Villes industrielles** (Beijing, Chengdu, Xi'an) : Niveaux élevés de SO₂ et PM2.5.
- **Métropoles à fort trafic** (Delhi, Mumbai, Bangkok) : NO₂ élevé, CO modéré.
- **Villes désertiques** (Riyadh, Dubai, Doha) : PM10 dominant, peu de NO₂.
- **Villes européennes** (Londres, Berlin) : Niveaux faibles sur tous les polluants, NO₂ est le principal problème.

---

## 5. Conclusions

### 5.1 Constats principaux

1. **La pollution de l'air est un problème urbain global** — 77% des mesures dépassent le seuil "Good".
2. **L'Asie du Sud est l'épicentre de la crise** — Delhi, Lahore et Dhaka affichent des niveaux d'AQI 5 à 10 fois supérieurs aux recommandations de l'OMS.
3. **Les particules fines (PM2.5) sont le polluant le plus préoccupant** — leur concentration élevée et leur impact sanitaire documenté en font une priorité.
4. **Les conditions météorologiques amplifient la pollution** — l'hiver aggrave la situation dans la majorité des régions.
5. **Les disparités régionales sont très marquées** — les villes d'Europe et d'Océanie bénéficient d'un air bien plus sain que les villes asiatiques ou africaines.

### 5.2 Forces et limites du dashboard

**Forces :**
- Vision globale et locale de la pollution
- Filtres interactifs permettant l'exploration autonome
- Corrélation entre AQI, polluants, température et saison
- Carte géographique pour la dimension spatiale

**Limites identifiées :**
- Données simulées (non issues de capteurs réels)
- Période limitée à 2 ans (tendance long terme non visible)
- Absence de données démographiques (impact sanitaire non quantifiable)

---

## 6. Recommandations

### 6.1 Recommandations opérationnelles

| Priorité | Action | Cible | Impact attendu |
|----------|--------|-------|----------------|
| 🔴 1 | Réduire les émissions de PM2.5 des transports et de l'industrie | Villes asiatiques | ↓ 20-30% AQI |
| 🟠 2 | Mettre en place des zones à faibles émissions (ZFE) | Delhi, Lahore, Dhaka | ↓ 15% NO₂ |
| 🟠 3 | Interdire le brûlage agricole post-récolte | Inde, Pakistan | ↓ 40% PM2.5 en automne |
| 🟡 4 | Développer les transports propres (électrique, métro) | Toutes grandes villes | ↓ 25% CO, NO₂ |
| 🟡 5 | Installer des systèmes d'alerte précoce | Populations sensibles | Réduction des risques sanitaires |
| 🟢 6 | Planter des arbres et créer des corridors verts | Zones urbannes denses | ↓ 10% PM10 |

### 6.2 Recommandations pour l'analyse future

1. **Intégrer des données sanitaires** (hospitalisations, mortalité) pour mesurer l'impact réel.
2. **Étendre la couverture temporelle** à 5-10 ans pour identifier les tendances de fond.
3. **Ajouter des indicateurs économiques** (coût sanitaire, perte de productivité) pour renforcer l'argumentaire.
4. **Connecter le dashboard à des données en temps réel** (API des stations de mesure) pour un suivi live.
5. **Déployer un modèle prédictif** (ML) pour anticiper les pics de pollution à 48h.

### 6.3 Message clé

> **"La pollution de l'air n'est pas une fatalité. Les données montrent que les villes qui agissent (restrictions de circulation, énergies propres, végétalisation) obtiennent des résultats mesurables. Ce dashboard vise à éclairer les décisions des citoyens, des chercheurs et des décideurs."**

---

## Annexe : Palette de couleurs AQI (Standard EPA)

```
Good        (0-50)    🟢 #00E400
Moderate    (51-100)  🟡 #FFFF00
USG         (101-150) 🟠 #FF7E00
Unhealthy   (151-200) 🔴 #FF0000
Very Unhealthy(201-300) 🟣 #8F3F97
Hazardous   (301-500) 🟤 #7E0023
```

---

*Document généré le 23 juillet 2026 dans le cadre du Projet AQI — Bloc 2 : Visualisation de données.*
