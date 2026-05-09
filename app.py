import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Dengue Intelligent Dashboard (DID)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# Custom Styling
# -----------------------------------
st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #2b0000, #7a0000, #c1121f);
    color: white;
}

section[data-testid="stSidebar"] {
    background: rgba(20,20,20,0.95);
    border-right: 1px solid rgba(255,255,255,0.1);
}

.glass-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

h1, h2, h3, h4, p, label {
    color: white !important;
}

.metric-box {
    background: rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 15px;
}

.alert-high {
    background-color: rgba(255, 0, 0, 0.25);
    border-left: 5px solid red;
    padding: 15px;
    border-radius: 12px;
}

.alert-medium {
    background-color: rgba(255, 165, 0, 0.25);
    border-left: 5px solid orange;
    padding: 15px;
    border-radius: 12px;
}

.alert-low {
    background-color: rgba(0, 255, 0, 0.15);
    border-left: 5px solid green;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Sidebar Login
# -----------------------------------
st.sidebar.title("🔐 Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

login_btn = st.sidebar.button("Login")

if login_btn:
    st.sidebar.success(f"Welcome {username}")

st.sidebar.markdown("---")
st.sidebar.write("DID System v1")
st.sidebar.write(datetime.now().strftime("%Y-%m-%d"))

# -----------------------------------
# Header
# -----------------------------------
st.markdown("""
<div class="glass-card">
    <h1>🦟 Dengue Intelligent Dashboard (DID)</h1>
    <p>AI-Powered Early Warning System for Dengue Fever in Sudan</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------------
# Dashboard Layout
# -----------------------------------
col1, col2 = st.columns([2, 1])

# -----------------------------------
# Interactive Map
# -----------------------------------
with col1:
    st.markdown("""
    <div class="glass-card">
        <h2>🗺 Interactive Risk Map</h2>
    """, unsafe_allow_html=True)

    # Create map
    m = folium.Map(location=[15.55, 32.55], zoom_start=6)

    # Example markers
    folium.CircleMarker(
        location=[15.60, 32.53],
        radius=12,
        popup="Khartoum - High Risk",
        color="red",
        fill=True,
        fill_color="red"
    ).add_to(m)

    folium.CircleMarker(
        location=[15.45, 32.40],
        radius=10,
        popup="Omdurman - Medium Risk",
        color="orange",
        fill=True,
        fill_color="orange"
    ).add_to(m)

    folium.CircleMarker(
        location=[15.70, 32.65],
        radius=8,
        popup="Bahri - Low Risk",
        color="green",
        fill=True,
        fill_color="green"
    ).add_to(m)

    st_folium(m, width=900, height=500)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------
# Alerts Panel
# -----------------------------------
with col2:
    st.markdown("""
    <div class="glass-card">
        <h2>🚨 Early Warning Alerts</h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-high">
        <strong>Critical Alert:</strong><br>
        High outbreak probability detected in Khartoum.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="alert-medium">
        <strong>Medium Risk:</strong><br>
        Increased mosquito activity in Omdurman.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="alert-low">
        <strong>Low Risk:</strong><br>
        Stable conditions in Bahri district.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------
# Statistics Section
# -----------------------------------
st.write("")

st.markdown("""
<div class="glass-card">
    <h2>📊 Dengue Cases Monitoring</h2>
</div>
""", unsafe_allow_html=True)

# Example dataset
data = pd.DataFrame({
    "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
    "Cases": [45, 78, 120, 95]
})

# Charts
chart_col1, chart_col2, chart_col3 = st.columns(3)

with chart_col1:
    st.markdown("""
    <div class="metric-box">
        <h3>Total Cases</h3>
        <h2>338</h2>
    </div>
    """, unsafe_allow_html=True)

with chart_col2:
    st.markdown("""
    <div class="metric-box">
        <h3>High Risk Districts</h3>
        <h2>5</h2>
    </div>
    """, unsafe_allow_html=True)

with chart_col3:
    st.markdown("""
    <div class="metric-box">
        <h3>Prediction Accuracy</h3>
        <h2>89%</h2>
    </div>
    """, unsafe_allow_html=True)

# Line chart
st.line_chart(data.set_index("Week"))

# Data table
st.dataframe(data, use_container_width=True)

# -----------------------------------
# Footer
# -----------------------------------
st.markdown("""
<hr>
<center>
<p style='color:white; opacity:0.7;'>
Dengue Intelligent Dashboard (DID) | Built with Streamlit + Folium + FastAPI Ready
</p>
</center>
""", unsafe_allow_html=True)
