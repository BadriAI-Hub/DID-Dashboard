import streamlit as st
import pandas as pd
import folium
import json
import random

from streamlit_folium import st_folium


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="DID Dashboard",
    layout="wide"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #2b0000,
            #7f0000,
            #c1121f
        );
    }

    h1, h2, h3, h4, p, label {
        color: white !important;
    }

    .glass {
        background: rgba(255,255,255,0.08);

        backdrop-filter: blur(10px);

        border-radius: 20px;

        padding: 20px;

        margin-bottom: 20px;

        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }

    </style>
    """,
    unsafe_allow_html=True
)


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
    "Dengue Intelligent Dashboard"
)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div class="glass">

        <h1>
            🦟 Dengue Intelligent Dashboard
        </h1>

        <p>
            AI-Powered Early Warning System
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# METRICS
# =====================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Active Cases",
        "338"
    )

with m2:
    st.metric(
        "High Risk Areas",
        "18"
    )

with m3:
    st.metric(
        "Alerts",
        "12"
    )

with m4:
    st.metric(
        "Model Accuracy",
        "89%"
    )


# =====================================================
# MAIN LAYOUT
# =====================================================

left, right = st.columns([3,1])


# =====================================================
# INTERACTIVE SUDAN MAP
# =====================================================

with left:

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

    # -------------------------------------------------
    # CREATE MAP
    # -------------------------------------------------

    m = folium.Map(

        location=[15.5, 30.5],

        zoom_start=5,

        tiles="cartodbpositron"
    )



    # -------------------------------------------------
    # LOAD GEOJSON
    # -------------------------------------------------

    try:

        with open(
            "sudan_localities.geojson",
            "r",
            encoding="utf-8"
        ) as f:

            geojson_data = json.load(f)

    except Exception as e:

        st.error(
            f"GeoJSON Load Error: {e}"
        )

        geojson_data = None



    # -------------------------------------------------
    # RISK COLORS
    # -------------------------------------------------

    risk_colors = {

        "Critical": "#ff0000",

        "High": "#b71c1c",

        "Medium": "#ff9800",

        "Low": "#4caf50"
    }



    # -------------------------------------------------
    # CREATE DYNAMIC DATA
    # -------------------------------------------------

    locality_data = {}

    if geojson_data:

        for feature in geojson_data["features"]:

            locality_name = feature["properties"].get(
                "name",
                "Unknown"
            )

            risk = random.choice(
                [
                    "Critical",
                    "High",
                    "Medium",
                    "Low"
                ]
            )

            cases = random.randint(
                5,
                250
            )

            locality_data[locality_name] = {

                "risk": risk,

                "cases": cases,

                "color": risk_colors[risk]
            }



    # -------------------------------------------------
    # STYLE FUNCTION
    # -------------------------------------------------

    def style_function(feature):

        locality_name = feature["properties"].get(
            "name",
            "Unknown"
        )

        if locality_name in locality_data:

            return {

                "fillColor":
                locality_data[locality_name]["color"],

                "color": "white",

                "weight": 1.5,

                "fillOpacity": 0.7
            }

        return {

            "fillColor": "gray",

            "color": "white",

            "weight": 1,

            "fillOpacity": 0.3
        }



    # -------------------------------------------------
    # TOOLTIP
    # -------------------------------------------------

    tooltip = folium.GeoJsonTooltip(

        fields=["name"],

        aliases=["Locality:"],

        sticky=True
    )



    # -------------------------------------------------
    # ADD GEOJSON
    # -------------------------------------------------

    if geojson_data:

        folium.GeoJson(

            geojson_data,

            style_function=style_function,

            tooltip=tooltip

        ).add_to(m)



    # -------------------------------------------------
    # ADD CASE LABELS
    # -------------------------------------------------

    if geojson_data:

        for feature in geojson_data["features"]:

            locality_name = feature["properties"].get(
                "name",
                "Unknown"
            )

            geometry = feature["geometry"]

            try:

                coords = geometry["coordinates"]


                if geometry["type"] == "Polygon":

                    first_point = coords[0][0]

                    lon = first_point[0]

                    lat = first_point[1]


                elif geometry["type"] == "MultiPolygon":

                    first_point = coords[0][0][0]

                    lon = first_point[0]

                    lat = first_point[1]


                else:

                    continue


                cases = locality_data[
                    locality_name
                ]["cases"]


                folium.Marker(

                    location=[lat, lon],

                    icon=folium.DivIcon(

                        html=f"""
                        <div style='
                            font-size:14px;
                            font-weight:bold;
                            color:white;
                            background:red;
                            border-radius:50%;
                            width:32px;
                            height:32px;
                            text-align:center;
                            line-height:32px;
                            border:2px solid white;
                        '>

                        {cases}

                        </div>
                        """
                    )

                ).add_to(m)

            except:

                pass



    # -------------------------------------------------
    # DISPLAY MAP
    # -------------------------------------------------

    st_folium(
        m,
        width=1100,
        height=700
    )


# =====================================================
# ALERTS PANEL
# =====================================================

with right:

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

    st.error(
        "Critical outbreak probability detected"
    )

    st.warning(
        "Heavy rainfall expected this week"
    )

    st.warning(
        "Flood risk increasing near Nile areas"
    )

    st.info(
        "Mosquito density increased by 23%"
    )

    st.success(
        "Low risk zones remain stable"
    )


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📈 Forecast",
        "🌡 Climate",
        "🔍 SHAP"
    ]
)


# =====================================================
# FORECAST TAB
# =====================================================

with tab1:

    st.subheader(
        "📈 Multi-Variable Dengue Forecast"
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
        ],

        "Flood Risk": [
            1,
            1,
            2,
            2,
            3,
            3
        ],

        "Displacement Camps": [
            4,
            5,
            5,
            6,
            7,
            7
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
        st.metric(
            "Temperature",
            "34°C"
        )

    with c2:
        st.metric(
            "Humidity",
            "74%"
        )

    with c3:
        st.metric(
            "Rainfall",
            "22 mm"
        )

    with c4:
        st.metric(
            "NDVI",
            "0.61"
        )

    with c5:
        st.metric(
            "Flood Risk",
            "High"
        )


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
            "Displacement",
            "Temperature"
        ],

        "Importance": [
            0.42,
            0.30,
            0.15,
            0.08,
            0.03,
            0.02
        ]
    })

    st.bar_chart(
        shap_df.set_index("Factor")
    )


# =====================================================
# PIPELINE STATUS
# =====================================================

st.markdown(
    """
    <div class="glass">

        <h2>
            ⚙ Pipeline Status
        </h2>

    </div>
    """,
    unsafe_allow_html=True
)

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

st.markdown(
    """
    <hr>

    <center>

    <p style="color:white;">

        DID Prototype v4
        |
        Sudan GeoJSON + Folium + Streamlit

    </p>

    </center>
    """,
    unsafe_allow_html=True
)
