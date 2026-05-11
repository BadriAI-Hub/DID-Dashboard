import streamlit as st
import pandas as pd
import folium
import json

from streamlit_folium import st_folium


# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="DID Dashboard",
    layout="wide"
)


# ------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------

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

    .glass {
        background: rgba(255,255,255,0.08);

        backdrop-filter: blur(10px);

        border-radius: 20px;

        padding: 20px;

        margin-bottom: 20px;

        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }

    h1,h2,h3,h4,p,label {
        color: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("🔐 Login")

username = st.sidebar.text_input(
    "Username"
)

password = st.sidebar.text_input(
    "Password",
    type="password"
)

login_btn = st.sidebar.button(
    "Login"
)

if login_btn:

    st.sidebar.success(
        f"Welcome {username}"
    )

st.sidebar.markdown("---")

st.sidebar.write(
    "Dengue Intelligent Dashboard"
)


# ------------------------------------------------
# HEADER
# ------------------------------------------------

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


# ------------------------------------------------
# METRICS
# ------------------------------------------------

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Active Cases",
        "338"
    )

with m2:

    st.metric(
        "High Risk Areas",
        "5"
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


# ------------------------------------------------
# MAIN LAYOUT
# ------------------------------------------------

left, right = st.columns([2,1])


# ------------------------------------------------
# INTERACTIVE RISK MAP
# ------------------------------------------------

with left:

    st.markdown(
        """
        <div class="glass">

        <h2>
            🗺 Khartoum Dengue Risk Map
        </h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------
    # CREATE MAP
    # --------------------------------------------

    m = folium.Map(

        location=[15.55, 32.55],

        zoom_start=8,

        tiles="cartodbpositron"
    )



    # --------------------------------------------
    # RISK DATA
    # --------------------------------------------

    risk_data = {

        "Khartoum": {
            "risk": "Critical",
            "cases": 155,
            "color": "#ff0000"
        },

        "Omdurman": {
            "risk": "High",
            "cases": 120,
            "color": "#8b0000"
        },

        "Bahri": {
            "risk": "Medium",
            "cases": 78,
            "color": "#ff9800"
        },

        "Karari": {
            "risk": "High",
            "cases": 98,
            "color": "#b22222"
        },

        "East Nile": {
            "risk": "Medium",
            "cases": 65,
            "color": "#ffb347"
        },

        "Jabal Awliya": {
            "risk": "Low",
            "cases": 20,
            "color": "#4caf50"
        },

        "Sharg Elneel": {
            "risk": "Low",
            "cases": 18,
            "color": "#66bb6a"
        }
    }



    # --------------------------------------------
    # STYLE FUNCTION
    # --------------------------------------------

    def style_function(feature):

        district_name = feature["properties"]["name"]

        if district_name in risk_data:

            return {

                "fillColor":
                risk_data[district_name]["color"],

                "color": "white",

                "weight": 2,

                "fillOpacity": 0.7
            }

        return {

            "fillColor": "gray",

            "color": "white",

            "weight": 1,

            "fillOpacity": 0.3
        }



    # --------------------------------------------
    # LOAD GEOJSON FILE
    # --------------------------------------------

    with open(
        "khartoum_districts.geojson",
        "r",
        encoding="utf-8"
    ) as f:

        geojson_data = json.load(f)



    # --------------------------------------------
    # ADD GEOJSON
    # --------------------------------------------

    folium.GeoJson(

        geojson_data,

        style_function=style_function,

        tooltip=folium.GeoJsonTooltip(

            fields=["name"],

            aliases=["District:"]
        )

    ).add_to(m)



    # --------------------------------------------
    # ADD CASE NUMBERS
    # --------------------------------------------

    district_centers = {

        "Khartoum": [15.60, 32.53],

        "Omdurman": [15.45, 32.40],

        "Bahri": [15.70, 32.65],

        "Karari": [15.75, 32.30],

        "East Nile": [15.65, 32.75],

        "Jabal Awliya": [15.20, 32.30],

        "Sharg Elneel": [15.80, 32.80]
    }



    for district, coords in district_centers.items():

        folium.Marker(

            location=coords,

            icon=folium.DivIcon(

                html=f"""

                <div style='
                    font-size:18px;
                    font-weight:bold;
                    color:white;
                    background:red;
                    border-radius:50%;
                    width:35px;
                    height:35px;
                    text-align:center;
                    line-height:35px;
                    border:2px solid white;
                '>

                {risk_data[district]['cases']}

                </div>
                """
            )
        ).add_to(m)



    # --------------------------------------------
    # BLUE NILE
    # --------------------------------------------

    folium.PolyLine(

        [
            [15.9,32.4],
            [15.7,32.5],
            [15.5,32.55]
        ],

        color="blue",

        weight=6,

        tooltip="Blue Nile"

    ).add_to(m)



    # --------------------------------------------
    # WHITE NILE
    # --------------------------------------------

    folium.PolyLine(

        [
            [15.9,32.7],
            [15.7,32.6],
            [15.5,32.55]
        ],

        color="lightblue",

        weight=6,

        tooltip="White Nile"

    ).add_to(m)



    # --------------------------------------------
    # DISPLAY MAP
    # --------------------------------------------

    st_folium(

        m,

        width=900,

        height=600
    )


# ------------------------------------------------
# ALERTS
# ------------------------------------------------

with right:

    st.markdown(
        """
        <div class="glass">

        <h2>
            🚨 Alerts
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.error(
        "Critical outbreak probability in Khartoum"
    )

    st.warning(
        "High mosquito activity in Omdurman"
    )

    st.warning(
        "Flood risk increasing near Nile banks"
    )

    st.info(
        "Heavy rainfall expected this week"
    )

    st.success(
        "Low risk in Jabal Awliya"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ------------------------------------------------
# TABS
# ------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "📈 Forecast",
        "🌡 Climate",
        "🔍 SHAP"
    ]
)


# ------------------------------------------------
# FORECAST TAB
# ------------------------------------------------

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

        "Temperature °C": [
            31,
            32,
            34,
            35,
            36,
            37
        ],

        "Humidity %": [
            68,
            70,
            74,
            78,
            80,
            83
        ],

        "Rainfall mm": [
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

        "Stagnant Water Sites": [
            15,
            20,
            31,
            45,
            60,
            82
        ],

        "Displacement Camps": [
            4,
            5,
            5,
            6,
            7,
            7
        ],

        "Population Density": [
            1200,
            1210,
            1225,
            1230,
            1245,
            1260
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


# ------------------------------------------------
# CLIMATE TAB
# ------------------------------------------------

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


# ------------------------------------------------
# SHAP TAB
# ------------------------------------------------

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


# ------------------------------------------------
# PIPELINE STATUS
# ------------------------------------------------

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
    st.warning("3️⃣ LSTM")

with p4:
    st.success("4️⃣ Notifications")


# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown(
    """
    <hr>

    <center>

    <p style="color:white;">

        DID Prototype v3
        |
        Streamlit + GeoJSON + Folium + LSTM

    </p>

    </center>
    """,
    unsafe_allow_html=True
)
