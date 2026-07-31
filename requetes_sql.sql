/********************************************************************
 *  REQUÃŠTES SQL OPTIMISÃ‰ES - Dashboard AQI (Bloc 2)               *
 *  Data Warehouse : SchÃ©ma en Ã‰toile                              *
 *  Auteur : Data Analyst - Projet AQI                             *
 *  Date : Juillet 2026                                            *
 ********************************************************************/

-- ==================================================================
-- MODÃˆLE DE DONNÃ‰ES (DDL - CrÃ©ation des tables)
-- ==================================================================

-- Table de dimension : Villes
CREATE TABLE dim_city (
    city_id        INT PRIMARY KEY,
    city_name      VARCHAR(100) NOT NULL,
    country        VARCHAR(100) NOT NULL,
    latitude       DECIMAL(10,6),
    longitude      DECIMAL(10,6),
    population     INT,
    CONSTRAINT uq_city UNIQUE (city_name, country)
);

-- Table de dimension : Date
CREATE TABLE dim_date (
    date_id        INT PRIMARY KEY,
    date           DATE NOT NULL,
    year           SMALLINT NOT NULL,
    month          TINYINT NOT NULL,
    month_name     VARCHAR(20) NOT NULL,
    quarter        TINYINT NOT NULL,
    day_of_week    TINYINT,
    is_weekend     BIT DEFAULT 0,
    CONSTRAINT uq_date UNIQUE (date)
);

-- Table de dimension : Polluants
CREATE TABLE dim_pollutant (
    pollutant_id   INT PRIMARY KEY,
    pollutant_name VARCHAR(20) NOT NULL,
    unit           VARCHAR(10) NOT NULL,
    description    VARCHAR(200)
);

INSERT INTO dim_pollutant VALUES
    (1, 'PM2.5', 'Âµg/mÂ³', 'Particules fines < 2.5Âµm'),
    (2, 'PM10',  'Âµg/mÂ³', 'Particules < 10Âµm'),
    (3, 'NOâ‚‚',   'ppb',   'Dioxyde d''azote'),
    (4, 'SOâ‚‚',   'ppb',   'Dioxyde de soufre'),
    (5, 'CO',    'ppm',   'Monoxyde de carbone'),
    (6, 'Oâ‚ƒ',    'ppb',   'Ozone troposphÃ©rique');

-- Table de faits : Mesures AQI
CREATE TABLE fact_aqi (
    measurement_id   BIGINT PRIMARY KEY,
    city_id          INT NOT NULL REFERENCES dim_city(city_id),
    date_id          INT NOT NULL REFERENCES dim_date(date_id),
    aqi_value        INT NOT NULL CHECK (aqi_value BETWEEN 0 AND 500),
    aqi_category     VARCHAR(40) NOT NULL,
    pm25             DECIMAL(8,2),
    pm10             DECIMAL(8,2),
    no2              DECIMAL(8,2),
    so2              DECIMAL(8,2),
    co               DECIMAL(8,2),
    o3               DECIMAL(8,2),
    temperature      DECIMAL(5,1),
    humidity         DECIMAL(5,1),
    CONSTRAINT fk_fact_city FOREIGN KEY (city_id) REFERENCES dim_city(city_id),
    CONSTRAINT fk_fact_date FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- Index pour optimiser les performances des requÃªtes du dashboard
CREATE INDEX idx_fact_aqi_city   ON fact_aqi(city_id);
CREATE INDEX idx_fact_aqi_date   ON fact_aqi(date_id);
CREATE INDEX idx_fact_aqi_value  ON fact_aqi(aqi_value);
CREATE INDEX idx_fact_aqi_cat    ON fact_aqi(aqi_category);
CREATE INDEX idx_dim_date_year   ON dim_date(year);
CREATE INDEX idx_dim_date_month  ON dim_date(month);


-- ==================================================================
-- REQUÊTES SQL POUR LE DASHBOARD
-- ==================================================================

-- ----------------------------------------------------------------
-- 1. CARTES KPI
-- ----------------------------------------------------------------

-- 1a. AQI Moyen (global)
SELECT ROUND(AVG(aqi_value), 1) AS aqi_moyen
FROM fact_aqi
WHERE aqi_value IS NOT NULL;

-- 1b. AQI Maximum
SELECT MAX(aqi_value) AS aqi_maximum
FROM fact_aqi;

-- 1c. AQI Minimum
SELECT MIN(aqi_value) AS aqi_minimum
FROM fact_aqi
WHERE aqi_value > 0;

-- 1d. Nombre total de mesures
SELECT COUNT(*) AS total_mesures
FROM fact_aqi;

-- 1e. Nombre de villes analysées
SELECT COUNT(DISTINCT c.city_name) AS nb_villes
FROM fact_aqi f
JOIN dim_city c ON f.city_id = c.city_id;

-- 1f. KPI avec filtres dynamiques (exemple avec paramètres)
-- Utiliser des paramètres SQL ou des variables selon le SGBD
-- DECLARE @ville VARCHAR(100) = NULL
-- DECLARE @pays   VARCHAR(100) = NULL
-- DECLARE @debut  DATE = '2023-01-01'
-- DECLARE @fin    DATE = '2024-12-31'

SELECT
    ROUND(AVG(f.aqi_value), 1) AS aqi_moyen,
    MAX(f.aqi_value)           AS aqi_maximum,
    MIN(f.aqi_value)           AS aqi_minimum,
    COUNT(*)                   AS total_mesures,
    COUNT(DISTINCT c.city_name) AS nb_villes
FROM fact_aqi f
JOIN dim_city c ON f.city_id = c.city_id
JOIN dim_date d ON f.date_id = d.date_id
WHERE (c.city_name = @ville OR @ville IS NULL)
  AND (c.country   = @pays  OR @pays  IS NULL)
  AND d.date BETWEEN @debut AND @fin;


-- ----------------------------------------------------------------
-- 2. ÉVOLUTION DE L'AQI DANS LE TEMPS (Line Chart)
-- ----------------------------------------------------------------

-- 2a. Agrégation mensuelle pour la courbe d'évolution
SELECT
    d.date,
    d.year,
    d.month,
    d.month_name,
    ROUND(AVG(f.aqi_value), 1) AS aqi_moyen,
    ROUND(AVG(f.pm25), 1)      AS pm25_moyen,
    ROUND(AVG(f.pm10), 1)      AS pm10_moyen,
    ROUND(AVG(f.no2), 1)       AS no2_moyen,
    ROUND(AVG(f.so2), 2)       AS so2_moyen,
    ROUND(AVG(f.co), 3)        AS co_moyen,
    ROUND(AVG(f.o3), 1)        AS o3_moyen
FROM fact_aqi f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.date, d.year, d.month, d.month_name
ORDER BY d.date;

-- 2b. Évolution par ville (préparé pour les filtres)
SELECT
    d.date,
    c.city_name,
    c.country,
    ROUND(AVG(f.aqi_value), 1) AS aqi_moyen
FROM fact_aqi f
JOIN dim_city c ON f.city_id = c.city_id
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.date, c.city_name, c.country
ORDER BY d.date, c.city_name;


-- ----------------------------------------------------------------
-- 3. AQI MOYEN PAR VILLE (Bar Chart)
-- ----------------------------------------------------------------

SELECT
    c.city_name,
    c.country,
    ROUND(AVG(f.aqi_value), 1) AS aqi_moyen,
    ROUND(AVG(f.pm25), 1)      AS pm25_moyen,
    COUNT(*)                   AS nb_mesures
FROM fact_aqi f
JOIN dim_city c ON f.city_id = c.city_id
GROUP BY c.city_name, c.country
ORDER BY aqi_moyen DESC;


-- ----------------------------------------------------------------
-- 4. TOP 10 DES VILLES LES PLUS POLLUÉES
-- ----------------------------------------------------------------

SELECT TOP 10
    c.city_name,
    c.country,
    ROUND(AVG(f.aqi_value), 1) AS aqi_moyen,
    ROUND(AVG(f.pm25), 1)      AS pm25_moyen,
    MAX(f.aqi_value)            AS aqi_max,
    COUNT(*)                    AS nb_mesures
FROM fact_aqi f
JOIN dim_city c ON f.city_id = c.city_id
GROUP BY c.city_name, c.country
ORDER BY aqi_moyen DESC;

-- Version compatible MySQL/PostgreSQL (LIMIT)
/*
SELECT
    c.city_name,
    c.country,
    ROUND(AVG(f.aqi_value), 1) AS aqi_moyen,
    ROUND(AVG(f.pm25), 1)      AS pm25_moyen,
    MAX(f.aqi_value)            AS aqi_max,
    COUNT(*)                    AS nb_mesures
FROM fact_aqi f
JOIN dim_city c ON f.city_id = c.city_id
GROUP BY c.city_name, c.country
ORDER BY aqi_moyen DESC
LIMIT 10;
*/


-- ----------------------------------------------------------------
-- 5. RÉPARTITION DES CATÉGORIES AQI (Donut Chart)
-- ----------------------------------------------------------------

SELECT
    f.aqi_category,
    COUNT(*)                                    AS nb_mesures,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pourcentage,
    CASE
        WHEN f.aqi_category = 'Good'                          THEN '#00E400'
        WHEN f.aqi_category = 'Moderate'                      THEN '#FFFF00'
        WHEN f.aqi_category = 'Unhealthy for Sensitive Groups' THEN '#FF7E00'
        WHEN f.aqi_category = 'Unhealthy'                     THEN '#FF0000'
        WHEN f.aqi_category = 'Very Unhealthy'                THEN '#8F3F97'
        WHEN f.aqi_category = 'Hazardous'                     THEN '#7E0023'
    END AS couleur_hex
FROM fact_aqi f
GROUP BY f.aqi_category
ORDER BY nb_mesures DESC;


-- ----------------------------------------------------------------
-- 6. COMPARAISON DES POLLUANTS PRINCIPAUX (Bar Chart / Radar)
-- ----------------------------------------------------------------

-- 6a. Moyenne de chaque polluant (unpivot)
SELECT 'PM2.5' AS polluant, ROUND(AVG(pm25), 2) AS valeur_moyenne, 'µg/m³' AS unite FROM fact_aqi
UNION ALL
SELECT 'PM10',  ROUND(AVG(pm10), 2), 'µg/m³' FROM fact_aqi
UNION ALL
SELECT 'NO2',   ROUND(AVG(no2),  2), 'ppb'   FROM fact_aqi
UNION ALL
SELECT 'SO2',   ROUND(AVG(so2),  2), 'ppb'   FROM fact_aqi
UNION ALL
SELECT 'CO',    ROUND(AVG(co),   3), 'ppm'   FROM fact_aqi
UNION ALL
SELECT 'O3',    ROUND(AVG(o3),   2), 'ppb'   FROM fact_aqi
ORDER BY valeur_moyenne DESC;

-- 6b. Évolution temporelle des polluants (pour Multi-line Chart)
SELECT
    d.date,
    ROUND(AVG(f.pm25), 1) AS pm25,
    ROUND(AVG(f.pm10), 1) AS pm10,
    ROUND(AVG(f.no2),  1) AS no2,
    ROUND(AVG(f.so2),  2) AS so2,
    ROUND(AVG(f.co),   3) AS co,
    ROUND(AVG(f.o3),   1) AS o3
FROM fact_aqi f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.date
ORDER BY d.date;


-- ----------------------------------------------------------------
-- 7. HEATMAP : PÉRIODES LES PLUS POLLUÉES (Mois × Année)
-- ----------------------------------------------------------------

-- 7a. Agrégation par mois et année (pour heatmap)
SELECT
    d.year,
    d.month,
    d.month_name,
    d.quarter,
    ROUND(AVG(f.aqi_value), 1) AS aqi_moyen,
    MAX(f.aqi_value)            AS aqi_max,
    COUNT(*)                    AS nb_mesures,
    CASE
        WHEN AVG(f.aqi_value) <= 50  THEN 'Good'
        WHEN AVG(f.aqi_value) <= 100 THEN 'Moderate'
        WHEN AVG(f.aqi_value) <= 150 THEN 'Unhealthy for Sensitive Groups'
        WHEN AVG(f.aqi_value) <= 200 THEN 'Unhealthy'
        WHEN AVG(f.aqi_value) <= 300 THEN 'Very Unhealthy'
        ELSE 'Hazardous'
    END AS categorie_moyenne
FROM fact_aqi f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name, d.quarter
ORDER BY d.year, d.month;

-- 7b. Périodes critiques (AQI > 150)
SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(*)                                AS nb_jours_critiques,
    ROUND(AVG(f.aqi_value), 1)              AS aqi_moyen_periode,
    ROUND(100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM fact_aqi f2
         JOIN dim_date d2 ON f2.date_id = d2.date_id
         WHERE d2.year = d.year AND d2.month = d.month), 1) AS pct_critique
FROM fact_aqi f
JOIN dim_date d ON f.date_id = d.date_id
WHERE f.aqi_value > 150  -- Unhealthy ou pire
GROUP BY d.year, d.month, d.month_name
ORDER BY nb_jours_critiques DESC;
