/********************************************************************
 *  REQUÊTES SQL OPTIMISÉES - Dashboard AQI (Bloc 2)               *
 *  Data Warehouse : Schéma en Étoile                              *
 *  Auteur : Data Analyst - Projet AQI                             *
 *  Date : Juillet 2026                                            *
 ********************************************************************/

-- ==================================================================
-- MODÈLE DE DONNÉES (DDL - Création des tables)
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
    (1, 'PM2.5', 'µg/m³', 'Particules fines < 2.5µm'),
    (2, 'PM10',  'µg/m³', 'Particules < 10µm'),
    (3, 'NO₂',   'ppb',   'Dioxyde d''azote'),
    (4, 'SO₂',   'ppb',   'Dioxyde de soufre'),
    (5, 'CO',    'ppm',   'Monoxyde de carbone'),
    (6, 'O₃',    'ppb',   'Ozone troposphérique');

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

-- Index pour optimiser les performances des requêtes du dashboard
CREATE INDEX idx_fact_aqi_city   ON fact_aqi(city_id);
CREATE INDEX idx_fact_aqi_date   ON fact_aqi(date_id);
CREATE INDEX idx_fact_aqi_value  ON fact_aqi(aqi_value);
CREATE INDEX idx_fact_aqi_cat    ON fact_aqi(aqi_category);
CREATE INDEX idx_dim_date_year   ON dim_date(year);
CREATE INDEX idx_dim_date_month  ON dim_date(month);
