import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title="Dashboard AQI", page_icon=":earth_africa:", layout="wide")

AQI_COLORS = {
    "Good": "#00E400",
    "Moderate": "#FFFF00",
    "Unhealthy for Sensitive Groups": "#FF7E00",
    "Unhealthy": "#FF0000",
    "Very Unhealthy": "#8F3F97",
    "Hazardous": "#7E0023"
}
CAT_ORDER = ["Good", "Moderate", "Unhealthy for Sensitive Groups",
             "Unhealthy", "Very Unhealthy", "Hazardous"]

POLLU_THRESHOLDS = {"PM2.5": 15, "PM10": 45, "NO2": 13, "SO2": 15, "CO": 4, "O3": 51}
POLLU_KEYS = ["pm25", "pm10", "no2", "so2", "co", "o3"]

@st.cache_data
def load_data():
    url = st.secrets["db_url"]
    engine = create_engine(url)
    df = pd.read_sql("SELECT * FROM fact_aqi ORDER BY date", engine)
    df["date"] = pd.to_datetime(df["date"])
    engine.dispose()
    return df

df = load_data()

st.markdown("""
<h1 style='text-align:center; color:#1B2A4A; padding:20px 0; border-bottom:3px solid #1B2A4A; margin-bottom:20px;'>
    Dashboard AQI &mdash; Qualit&eacute; de l&rsquo;Air
</h1>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Filtres")
    villes_f = st.multiselect("Ville", sorted(df["city_name"].unique()))
    pays_f = st.multiselect("Pays", sorted(df["country"].unique()))
    dr = st.date_input("Periode", [df["date"].min(), df["date"].max()],
                       min_value=df["date"].min(), max_value=df["date"].max())
    cat_f = st.multiselect("Categorie AQI", sorted(df["aqi_category"].unique()))

mask = pd.Series(True, index=df.index)
if villes_f: mask &= df["city_name"].isin(villes_f)
if pays_f: mask &= df["country"].isin(pays_f)
if len(dr) == 2:
    mask &= (df["date"] >= pd.Timestamp(dr[0])) & (df["date"] <= pd.Timestamp(dr[1]))
if cat_f: mask &= df["aqi_category"].isin(cat_f)

d = df[mask].copy()
if d.empty:
    st.warning("Aucune donnee pour les filtres selectionnes.")
    st.stop()

avg = round(d["aqi_value"].mean(), 1)
mx = d["aqi_value"].max()
mn = d["aqi_value"].min()
tt = len(d)
nv = d["city_name"].nunique()

pol = pd.DataFrame({
    "polluant": ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"],
    "valeur": [
        d["pm25"].mean(), d["pm10"].mean(),
        d["no2"].mean(), d["so2"].mean(),
        d["co"].mean(), d["o3"].mean()
    ]
})
dominant_idx = pol["valeur"].values / [POLLU_THRESHOLDS[p] for p in pol["polluant"]]
dominant_polluant = pol.loc[dominant_idx.argmax(), "polluant"]

def kc(v):
    if v <= 50: return "#00E400"
    if v <= 100: return "#FFFF00"
    if v <= 150: return "#FF7E00"
    if v <= 200: return "#FF0000"
    if v <= 300: return "#8F3F97"
    return "#7E0023"

kpis = [
    ("AQI MOYEN", avg, kc(avg)),
    ("AQI MAXIMUM", mx, "#FF0000"),
    ("AQI MINIMUM", mn, "#00E400"),
    ("TOTAL MESURES", f"{tt:,}", "#1B2A4A"),
    ("VILLES ANALYSEES", nv, "#1B2A4A"),
    ("POLLUANT DOMINANT", dominant_polluant, "#8F3F97")
]
cols = st.columns(len(kpis))
for i, (lb, vl, cl) in enumerate(kpis):
    fsize = 20 if i == len(kpis) - 1 else 28
    with cols[i]:
        st.markdown(f"""
        <div style='background:{cl}15;border-left:5px solid {cl};padding:15px;border-radius:5px;'>
            <p style='margin:0;font-size:12px;color:#666;'>{lb}</p>
            <p style='margin:0;font-size:{fsize}px;font-weight:bold;color:{cl};'>{vl}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#999;'>Projet AQI &mdash; Bloc 2 : Visualisation de donnees &mdash; Juillet 2026</p>", unsafe_allow_html=True)
