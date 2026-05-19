import streamlit as st
import folium
import json
import random
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
# CUSTOM CSS
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

h1,h2,h3,h4,p,label{
    color:white !important;
}

.glass{
    background: rgba(255,255,255,0.08);

    padding:20px;

    border-radius:20px;

    backdrop-filter: blur(10px);

    margin-bottom:20px;
}

[data-testid="metric-container"]{
    background: rgba(255,255,255,0.08);
    border-radius:15px;
    padding:15px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🔐 Login")

username = st.sidebar.text_input(
    "Username"
)

password = st.sidebar.text_input(
    "Password",
    type="password"
)

if st.sidebar.button("Login"):

    st.sidebar.success(
        f"Welcome {username}"
    )

st.sidebar.markdown("---")

st.sidebar.write(
    "DID Early Warning System"
)


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="glass">

<h1>
🦟 Sudan Dengue Intelligence Dashboard
</h1>

<p>
AI-Powered Early Warning & Climate Surveillance System
</p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# METRICS
# =====================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Active Cases", "338")

with m2:
    st.metric("High Risk Areas", "18")

with m3:
    st.metric("Alerts", "12")

with m4:
    st.metric("Model Accuracy", "89%")


# =====================================================
# MAP SECTION
# =====================================================

st.markdown("""
<div class="glass">

<h2>
🗺 Sudan Dengue Risk Map
</h2>

</div>
""", unsafe_allow_html=True)


# =====================================================
# CREATE MAP
# =====================================================

m = folium.Map(

    location=[15.5, 30.5],

    zoom_start=5,

    tiles="cartodbpositron"
)


# =====================================================
# LOAD GEOJSON
# =====================================================

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


# =====================================================
# GENERATE RISK DATA
# =====================================================

risk_data = {}

if geojson_data:

    for feature in geojson_data["features"]:

        try:

            properties = feature.get(
                "properties",
                {}
            )

            # -----------------------------------------
            # IMPORTANT:
            # change NAME_2 if needed
            # -----------------------------------------

            locality = properties.get(
                "NAME_2",
                ""
            )

            risk = random.choice([
                "Critical",
                "High",
                "Medium",
                "Low",
                "None"
            ])

            if risk == "Critical":

                color = "#ff0000"

            elif risk == "High":

                color = "#b30000"

            elif risk == "Medium":

                color = "#ff9800"

            elif risk == "Low":

                color = "#4caf50"

            else:

                color = "#d9d9d9"

            cases = random.randint(
                5,
                250
            )

            risk_data[locality] = {

                "risk": risk,

                "color": color,

                "cases": cases
            }

        except:

            pass


# =====================================================
# DRAW FEATURES
# =====================================================

if geojson_data:

    for feature in geojson_data["features"]:

        try:

            properties = feature.get(
                "properties",
                {}
            )

            locality = properties.get(
                "NAME_2",
                ""
            )

            risk_info = risk_data.get(
                locality,
                {}
            )

            color = risk_info.get(
                "color",
                "#d9d9d9"
            )

            risk_level = risk_info.get(
                "risk",
                "None"
            )

            cases = risk_info.get(
                "cases",
                0
            )

            folium.GeoJson(

                feature,

                style_function=lambda x,
                color=color: {

                    "fillColor": color,

                    "color": "white",

                    "weight": 1,

                    "fillOpacity": 0.7
                },

                tooltip=f"""
                {locality}
                | Risk: {risk_level}
                | Cases: {cases}
                """

            ).add_to(m)

        except:

            pass


# =====================================================
# SHOW MAP
# =====================================================

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

st.error(
    "Critical outbreak probability detected"
)

st.warning(
    "Heavy rainfall expected"
)

st.warning(
    "Flood risk increasing"
)

st.info(
    "Mosquito density increased"
)

st.success(
    "Low risk areas stable"
)


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "📈 Forecast",
    "🌡 Climate",
    "🔍 SHAP"
])


# =====================================================
# FORECAST TAB
# =====================================================

with tab1:

    st.subheader(
        "📈 Multi-Variable Forecast"
    )

    forecast_df = pd.DataFrame({

        "Week": [
            "W1",
            "W2",
            "W3",
            "W4",
            "W5",
            "W6"
        ],

        "Actual Cases": [
            45,
            72,
            118,
            155,
            None,
            None
        ],

        "Predicted Cases": [
            50,
            75,
            120,
            165,
            210,
            260
        ],

        "Temperature": [
            31,
            32,
            34,
            35,
            36,
            37
        ],

        "Humidity": [
            68,
            70,
            74,
            78,
            80,
            83
        ],

        "Rainfall": [
            12,
            18,
            25,
            30,
            42,
            55
        ],

        "NDVI": [
            0.42,
            0.48,
            0.53,
            0.61,
            0.66,
            0.72
        ]
    })

    st.line_chart(
        forecast_df.set_index("Week")[
            [
                "Actual Cases",
                "Predicted Cases"
            ]
        ]
    )

    st.dataframe(
        forecast_df,
        use_container_width=True
    )


# =====================================================
# CLIMATE TAB
# =====================================================

with tab2:

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric("Temperature", "34°C")

    with c2:
        st.metric("Humidity", "74%")

    with c3:
        st.metric("Rainfall", "22 mm")

    with c4:
        st.metric("NDVI", "0.61")

    with c5:
        st.metric("Flood Risk", "High")


# =====================================================
# SHAP TAB
# =====================================================

with tab3:

    shap_df = pd.DataFrame({

        "Factor": [
            "Rainfall",
            "Humidity",
            "NDVI",
            "Flood Risk",
            "Temperature"
        ],

        "Importance": [
            0.42,
            0.30,
            0.15,
            0.08,
            0.05
        ]
    })

    st.bar_chart(
        shap_df.set_index("Factor")
    )


# =====================================================
# PIPELINE STATUS
# =====================================================

st.markdown("""
<div class="glass">

<h2>
⚙ Pipeline Status
</h2>

</div>
""", unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.success("1️⃣ Ingestion")

with p2:
    st.info("2️⃣ Processing")

with p3:
    st.warning("3️⃣ LSTM Prediction")

with p4:
    st.success("4️⃣ Notifications")


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<hr>

<center>

<p style='color:white;'>

DID Prototype Stable Version
|
Sudan GeoJSON + Streamlit + Folium

</p>

</center>
""", unsafe_allow_html=True)
