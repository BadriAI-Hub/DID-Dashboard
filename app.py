import streamlit as st
import pandas as pd
import folium
import json

from streamlit_folium import st_folium


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="DID Dashboard",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

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


# ==================================================
# SIDEBAR
# ==================================================

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
    "DID System v3"
)


# ==================================================
# HEADER
# ==================================================

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


# ==================================================
# METRICS
# ==================================================

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


# ==================================================
# MAIN LAYOUT
# ==================================================

left, right = st.columns([2,1])


# ==================================================
# MAP
# ==================================================

with left:

    st.markdown(
        """
        <div class="glass">

        <h2>
            🗺 Khartoum Risk Map
        </h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    m = folium.Map(

        location=[15.55, 32.55],

        zoom_start=8,

        tiles="cartodbpositron"
    )



    # ==============================================
    # RISK DATA
    # ==============================================

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



    # ==============================================
    # STYLE FUNCTION
    # ==============================================

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



    # ==============================================
    # LOAD GEOJSON
    # ==============================================

    try:

        with open(
            "khartoum_districts.geojson",
            "r",
            encoding="utf-8"
        ) as f:

            geojson_data = json.load(f)

        folium.GeoJson(

            geojson_data,

            style_function=style_function,

            tooltip=folium.GeoJsonTooltip(
                fields=["name"],
                aliases=["District:"]
            )

        ).add_to(m)

    except:

        st.warning(
            "GeoJSON file not found."
        )



    # ==============================================
    # DISTRICT NUMBERS
    # ==============================================

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



    # ==============================================
    # BLUE NILE
    # ==============================================

    folium.PolyLine(

        [
            [15.9, 32.4],
            [15.7, 32.5],
            [15.5, 32.55]
        ],

        color="blue",

        weight=6

    ).add_to(m)



    # ==============================================
    # WHITE NILE
    # ==============================================

    folium.PolyLine(

        [
            [15.9, 32.7],
            [15.7, 32.6],
            [15.5, 32.55]
        ],

        color="lightblue",

        weight=6

    ).add_to(m)



    # ==============================================
    # SHOW MAP
    # ==============================================

    st_folium(
        m,
        width=900,
        height=600
    )


# ==================================================
# ALERTS PANEL
# ==================================================

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


# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📈 Forecast",
        "🌡 Climate",
        "🔍 SHAP"
    ]
)


# ==================================================
# FORECAST TAB
# ==================================================

with tab1:

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


# ==================================================
# CLIMATE TAB
# ==================================================

with tab2:

    c1, c2, c3, c4 = st.columns(4)

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


# ==================================================
# SHAP TAB
# ==================================================

with tab3:

    shap_df = pd.DataFrame({

        "Factor": [
            "Rainfall",
            "Humidity",
            "NDVI",
            "Temperature"
        ],

        "Importance": [
            0.42,
            0.30,
            0.18,
            0.10
        ]
    })

    st.bar_chart(
        shap_df.set_index("Factor")
    )


# ==================================================
# PIPELINE STATUS
# ==================================================

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


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <hr>

    <center>

    <p style="color:white;">

        DID Prototype v3

    </p>

    </center>
    """,
    unsafe_allow_html=True
)
