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

st.markdown("---")
st.markdown("<p style='text-align:center; color:#999;'>Projet AQI &mdash; Bloc 2 : Visualisation de donnees &mdash; Juillet 2026</p>", unsafe_allow_html=True)
