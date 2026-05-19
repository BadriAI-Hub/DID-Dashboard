import streamlit as st
import folium
import json
import random

from streamlit_folium import st_folium


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Sudan Dengue Dashboard",
    layout="wide"
)


# ==========================================
# CSS
# ==========================================

st.markdown(
    """
    <style>

    .stApp{
        background: linear-gradient(
            135deg,
            #3a0000,
            #7f0000,
            #b30000
        );
    }

    h1,h2,h3,p{
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
    """,
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🔐 Login")

st.sidebar.text_input("Username")

st.sidebar.text_input(
    "Password",
    type="password"
)

st.sidebar.button("Login")


# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <div class="glass">

    <h1>
        🦟 Sudan Dengue Dashboard
    </h1>

    <p>
        AI Early Warning System
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# METRICS
# ==========================================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Cases", "338")
c2.metric("High Risk", "18")
c3.metric("Alerts", "12")
c4.metric("Accuracy", "89%")

# ==========================================
# STABLE SUDAN MAP
# ==========================================

st.markdown(
    """
    <div class="glass">

    <h2>
        🗺 Sudan Dengue Risk Map
    </h2>

    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# LOAD GEOJSON
# ==========================================

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


# ==========================================
# CREATE MAP
# ==========================================

m = folium.Map(

    location=[15.5, 30.5],

    zoom_start=5,

    tiles="cartodbpositron",

    control_scale=True
)


# ==========================================
# ONLY AFFECTED AREAS
# ==========================================

affected_areas = {

    "Khartoum": {
        "risk": "Critical",
        "cases": 240,
        "color": "#ff0000"
    },

    "Bahri": {
        "risk": "High",
        "cases": 180,
        "color": "#b30000"
    },

    "Omdurman": {
        "risk": "Medium",
        "cases": 95,
        "color": "#ff9800"
    },

    "Nyala": {
        "risk": "High",
        "cases": 150,
        "color": "#d32f2f"
    },

    "Port Sudan": {
        "risk": "Low",
        "cases": 40,
        "color": "#4caf50"
    }
}


# ==========================================
# STYLE FUNCTION
# ==========================================

def style_function(feature):

    locality = feature["properties"].get(
        "name",
        ""
    )

    # المناطق المصابة فقط
    if locality in affected_areas:

        return {

            "fillColor":
            affected_areas[locality]["color"],

            "color": "white",

            "weight": 1.5,

            "fillOpacity": 0.75
        }

    # بقية السودان
    return {

        "fillColor": "#d9d9d9",

        "color": "#888",

        "weight": 0.5,

        "fillOpacity": 0.15
    }


# ==========================================
# TOOLTIP
# ==========================================

def tooltip_function(feature):

    locality = feature["properties"].get(
        "name",
        "Unknown"
    )

    if locality in affected_areas:

        risk = affected_areas[locality]["risk"]

        cases = affected_areas[locality]["cases"]

        return f"""
        <b>{locality}</b><br>
        Risk: {risk}<br>
        Cases: {cases}
        """

    return locality


# ==========================================
# ADD GEOJSON
# ==========================================

if geojson_data:

    folium.GeoJson(

        geojson_data,

        style_function=style_function,

        tooltip=folium.GeoJsonTooltip(

            fields=["name"],

            aliases=["Locality:"]
        )

    ).add_to(m)


# ==========================================
# ADD CASE LABELS
# ==========================================

if geojson_data:

    for feature in geojson_data["features"]:

        locality = feature["properties"].get(
            "name",
            ""
        )

        # فقط المناطق المصابة
        if locality not in affected_areas:

            continue


        try:

            geometry = feature["geometry"]

            coords = geometry["coordinates"]


            if geometry["type"] == "Polygon":

                point = coords[0][0]

                lon = point[0]

                lat = point[1]


            elif geometry["type"] == "MultiPolygon":

                point = coords[0][0][0]

                lon = point[0]

                lat = point[1]

            else:

                continue


            cases = affected_areas[
                locality
            ]["cases"]


            color = affected_areas[
                locality
            ]["color"]


            folium.Marker(

                location=[lat, lon],

                icon=folium.DivIcon(

                    html=f"""
                    <div style='
                        font-size:14px;
                        font-weight:bold;
                        color:white;
                        background:{color};
                        border-radius:50%;
                        width:34px;
                        height:34px;
                        text-align:center;
                        line-height:34px;
                        border:2px solid white;
                        box-shadow:0 0 10px rgba(0,0,0,0.4);
                    '>

                    {cases}

                    </div>
                    """
                )

            ).add_to(m)

        except:

            pass


# ==========================================
# DISPLAY MAP
# ==========================================

st_folium(

    m,

    width="100%",

    height=700,

    returned_objects=[]
)
# ==========================================
# ALERTS
# ==========================================

st.markdown(
    """
    <div class="glass">

    <h2>
        🚨 Alerts
    </h2>

    </div>
    """,
    unsafe_allow_html=True
)

st.error("Critical outbreak probability detected")
st.warning("Flood risk increasing")
st.info("Heavy rainfall expected")
st.success("Low risk localities stable")


# ==========================================
# FORECAST
# ==========================================

st.markdown(
    """
    <div class="glass">

    <h2>
        📈 Forecast
    </h2>

    </div>
    """,
    unsafe_allow_html=True
)

forecast_data = {
    "Week": ["W1","W2","W3","W4"],
    "Cases": [55,120,180,260]
}

st.line_chart(forecast_data)


# ==========================================
# SHAP
# ==========================================

st.markdown(
    """
    <div class="glass">

    <h2>
        🔍 SHAP Analysis
    </h2>

    </div>
    """,
    unsafe_allow_html=True
)

shap_data = {
    "Factor":[
        "Rainfall",
        "Humidity",
        "NDVI",
        "Flood"
    ],

    "Importance":[
        0.42,
        0.31,
        0.18,
        0.09
    ]
}

st.bar_chart(
    {
        "Importance":[
            0.42,
            0.31,
            0.18,
            0.09
        ]
    }
)


# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <hr>

    <center>

    <p style='color:white;'>

    DID Prototype v5

    </p>

    </center>
    """,
    unsafe_allow_html=True
)
