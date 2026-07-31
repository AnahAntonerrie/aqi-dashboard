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

# Pre-calculations
daily = d.groupby("date", as_index=False)["aqi_value"].mean()
cats = d["aqi_category"].value_counts().reindex(CAT_ORDER, fill_value=0).reset_index()
cats.columns = ["cat", "n"]
cats["c"] = cats["cat"].map(AQI_COLORS)

hh = d.copy()
hh["y"] = hh["date"].dt.year
hh["m"] = hh["date"].dt.month
hp = hh.groupby(["y", "m"], as_index=False)["aqi_value"].mean()
hp = hp.pivot(index="y", columns="m", values="aqi_value").reindex(columns=range(1, 13))
hp.columns = ["Jan", "Fev", "Mar", "Avr", "Mai", "Juin",
              "Juil", "Aout", "Sep", "Oct", "Nov", "Dec"]

t1, t2, t3, t4 = st.tabs([" Temporel", " Villes", " Polluants", " Analyse"])

with t1:
    c1, c2 = st.columns([2, 1])
    with c1:
        fig = px.line(daily, x="date", y="aqi_value",
                      title="Evolution de l'AQI dans le Temps",
                      labels={"date": "Date", "aqi_value": "AQI Moyen"})
        fig.update_traces(line_color="#1B2A4A", line_width=2)
        fig.update_layout(hovermode="x unified", margin=dict(t=30))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = go.Figure(data=[go.Pie(
            labels=cats["cat"], values=cats["n"],
            marker=dict(colors=cats["c"]), hole=0.4,
            textinfo="label+percent", textposition="outside"
        )])
        fig.update_layout(title="Repartition des Categories AQI", showlegend=False, margin=dict(t=30))
        st.plotly_chart(fig, use_container_width=True)

    fig = px.imshow(hp, text_auto=".0f", aspect="auto",
                    color_continuous_scale=["#00E400", "#FFFF00", "#FF7E00", "#FF0000", "#8F3F97"],
                    title="Heatmap AQI par Mois/Annee",
                    labels={"x": "Mois", "y": "Annee"})
    fig.update_layout(margin=dict(t=30))
    st.plotly_chart(fig, use_container_width=True)

city = d.groupby("city_name", as_index=False)["aqi_value"].mean().sort_values("aqi_value", ascending=False)
top10 = city.head(10)

map_ok = True
try:
    md = d.groupby(["city_name", "country", "latitude", "longitude"], as_index=False).agg(
        aqi=("aqi_value", "mean"), nb=("aqi_value", "count"))
except Exception:
    map_ok = False

tbl = d.groupby(["city_name", "country"], as_index=False).agg(
    aqi_moyen=("aqi_value", "mean"),
    aqi_max=("aqi_value", "max"),
    nb_mesures=("aqi_value", "count")
).sort_values("aqi_moyen", ascending=False)
tbl["aqi_moyen"] = tbl["aqi_moyen"].round(1)
tbl.columns = ["Ville", "Pays", "AQI Moyen", "AQI Max", "Nb Mesures"]

with t2:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(city.head(20), x="aqi_value", y="city_name", orientation="h",
                     title="AQI Moyen par Ville (Top 20)",
                     labels={"aqi_value": "AQI Moyen", "city_name": ""},
                     color="aqi_value",
                     color_continuous_scale=["#00E400", "#FFFF00", "#FF7E00", "#FF0000", "#8F3F97"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, margin=dict(t=30))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(top10, x="city_name", y="aqi_value",
                     title="Top 10 des Villes les Plus Polluees",
                     labels={"city_name": "Ville", "aqi_value": "AQI Moyen"},
                     color="aqi_value",
                     color_continuous_scale=["#FF7E00", "#FF0000", "#8F3F97"])
        fig.update_layout(margin=dict(t=30))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Carte Geographique des Villes")
    if map_ok:
        try:
            fig = go.Figure(data=go.Scattergeo(
                lon=md["longitude"], lat=md["latitude"],
                text=md["city_name"],
                hovertext=md.apply(
                    lambda r: f"<b>{r['city_name']}</b><br>Pays: {r['country']}<br>AQI: {r['aqi']:.1f}<br>Mesures: {int(r['nb'])}",
                    axis=1),
                hoverinfo="text", mode="markers",
                marker=dict(
                    size=md["aqi"] / 10 + 5,
                    color=md["aqi"],
                    colorscale=[[0, "#00E400"], [0.2, "#FFFF00"], [0.4, "#FF7E00"],
                                [0.6, "#FF0000"], [0.8, "#8F3F97"], [1, "#7E0023"]],
                    cmin=0, cmax=300,
                    colorbar=dict(title="AQI Moyen"),
                    line=dict(width=1, color="white")
                )
            ))
            fig.update_geos(projection_type="natural earth", showcountries=True,
                           countrycolor="rgba(200,200,200,0.5)", coastlinecolor="rgba(150,150,150,0.5)")
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=500,
                             geo=dict(bgcolor="rgba(240,240,240,0.5)"))
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erreur carte: {e}")
            st.info("La carte necessite une connexion internet.")
    else:
        st.info("Donnees geographiques non disponibles.")

    st.markdown("### Classement Complet des Villes")
    fig_tbl = go.Figure(data=[go.Table(
        header=dict(values=list(tbl.columns), fill_color="#1B2A4A", font=dict(color="white", size=12), align="left"),
        cells=dict(values=[tbl[c] for c in tbl.columns], fill_color=["#f9f9f9", "#ebebeb"], align="left", font_size=11)
    )])
    fig_tbl.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=max(400, len(tbl) * 25 + 50))
    st.plotly_chart(fig_tbl, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#999;'>Projet AQI &mdash; Bloc 2 : Visualisation de donnees &mdash; Juillet 2026</p>", unsafe_allow_html=True)
