import streamlit as st
import folium
import json
import pandas as pd

from streamlit_folium import folium_static


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Sudan Dengue Dashboard",
    layout="wide"
)


# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #2b0000,
        #7f0000,
        #b30000
    );
}

h1,h2,h3,h4,p{
    color:white !important;
}

.glass{
    background: rgba(255,255,255,0.08);

    padding:20px;

    border-radius:20px;

    backdrop-filter: blur(10px);

    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🔐 Login")

st.sidebar.text_input("Username")

st.sidebar.text_input(
    "Password",
    type="password"
)

st.sidebar.button("Login")


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="glass">

<h1>
🦟 Sudan Dengue Dashboard
</h1>

<p>
AI Early Warning System
</p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# METRICS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Cases", "338")
c2.metric("High Risk", "18")
c3.metric("Alerts", "12")
c4.metric("Accuracy", "89%")


# =====================================================
# MAP
# =====================================================

st.markdown("""
<div class="glass">

<h2>
🗺 Sudan Risk Map
</h2>

</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------
# CREATE MAP
# -----------------------------------------------------

m = folium.Map(

    location=[15.5, 30.5],

    zoom_start=5,

    tiles="cartodbpositron"
)


# -----------------------------------------------------
# LOAD GEOJSON
# -----------------------------------------------------

geojson_data = None

try:

    with open(
        "sudan_localities.geojson",
        "r",
        encoding="utf-8"
    ) as f:

        geojson_data = json.load(f)

except Exception as e:

    st.error(f"GeoJSON Error: {e}")


# -----------------------------------------------------
# ONLY AFFECTED AREAS
# -----------------------------------------------------

affected_areas = {

    "Khartoum": "#ff0000",

    "Bahri": "#b30000",

    "Omdurman": "#ff9800",

    "Nyala": "#d32f2f",

    "Port Sudan": "#4caf50"
}


# -----------------------------------------------------
# DRAW FEATURES SAFELY
# -----------------------------------------------------

if geojson_data:

    for feature in geojson_data["features"]:

        try:

            locality = feature["properties"].get(
                "name",
                ""
            )

            # affected only
            if locality in affected_areas:

                color = affected_areas[locality]

                folium.GeoJson(

                    feature,

                    style_function=lambda x,
                    color=color: {

                        "fillColor": color,

                        "color": "white",

                        "weight": 1,

                        "fillOpacity": 0.7
                    }

                ).add_to(m)

            # other areas
            else:

                folium.GeoJson(

                    feature,

                    style_function=lambda x: {

                        "fillColor": "#d9d9d9",

                        "color": "#999",

                        "weight": 0.4,

                        "fillOpacity": 0.1
                    }

                ).add_to(m)

        except:

            pass


# -----------------------------------------------------
# SHOW MAP
# -----------------------------------------------------

folium_static(
    m,
    width=1200,
    height=700
)


# =====================================================
# ALERTS
# =====================================================

st.markdown("""
<div class="glass">

<h2>
🚨 Alerts
</h2>

</div>
""", unsafe_allow_html=True)

st.error("Critical outbreak probability detected")
st.warning("Heavy rainfall expected")
st.warning("Flood risk increasing")
st.info("Mosquito density increased")
st.success("Low risk areas stable")


# =====================================================
# FORECAST
# =====================================================

st.markdown("""
<div class="glass">

<h2>
📈 Forecast
</h2>

</div>
""", unsafe_allow_html=True)

forecast_df = pd.DataFrame({

    "Week": [
        "W1",
        "W2",
        "W3",
        "W4"
    ],

    "Predicted Cases": [
        55,
        120,
        180,
        260
    ]
})

st.line_chart(
    forecast_df.set_index("Week")
)


# =====================================================
# CLIMATE
# =====================================================

st.markdown("""
<div class="glass">

<h2>
🌡 Climate Indicators
</h2>

</div>
""", unsafe_allow_html=True)

cc1, cc2, cc3, cc4 = st.columns(4)

cc1.metric("Temperature", "34°C")
cc2.metric("Humidity", "74%")
cc3.metric("Rainfall", "22mm")
cc4.metric("NDVI", "0.61")


# =====================================================
# SHAP
# =====================================================

st.markdown("""
<div class="glass">

<h2>
🔍 SHAP Analysis
</h2>

</div>
""", unsafe_allow_html=True)

shap_df = pd.DataFrame({

    "Factor": [
        "Rainfall",
        "Humidity",
        "NDVI",
        "Flood Risk"
    ],

    "Importance": [
        0.42,
        0.31,
        0.18,
        0.09
    ]
})

st.bar_chart(
    shap_df.set_index("Factor")
)


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<hr>

<center>

<p style='color:white;'>

DID Prototype Stable Version

</p>

</center>
""", unsafe_allow_html=True)
