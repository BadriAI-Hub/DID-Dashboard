import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
st.set_page_config(page_title='DID Dashboard', layout='wide')

#-----------------------------

#THEME + STYLING

#-----------------------------

st.markdown("""

<style>
body {
    background: linear-gradient(135deg,#2b0000,#7f0000,#c1121f);
}

.glass-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}

.metric-box {
    background: rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 18px;
    text-align:center;
}

h1,h2,h3,h4,p,label {
    color:white !important;
}

.alert-box {
    padding:15px;
    border-radius:14px;
    margin-bottom:10px;
    color:white;
}

.critical {background:rgba(255,0,0,0.25);border-left:5px solid red;}
.high {background:rgba(255,80,80,0.25);border-left:5px solid darkred;}
.medium {background:rgba(255,165,0,0.25);border-left:5px solid orange;}
.low {background:rgba(0,255,0,0.15);border-left:5px solid green;}
</style>""", unsafe_allow_html=True)

#-----------------------------

#SIDEBAR LOGIN

#-----------------------------

st.sidebar.title('🔐 Login') username = st.sidebar.text_input('Username') password = st.sidebar.text_input('Password', type='password')

if st.sidebar.button('Login'): st.sidebar.success(f'Welcome {username}')

st.sidebar.markdown('---') st.sidebar.write('DID System v1') st.sidebar.write(datetime.now().strftime('%Y-%m-%d'))

#-----------------------------

#THEME TOGGLE

#-----------------------------

header1, header2 = st.columns([10,1]) with header2: st.button('🌓')

#-----------------------------

#HEADER

#-----------------------------

st.markdown("""

<div class='glass-card'>
<h1>🦟 Dengue Intelligent Dashboard (DID)</h1>
<p>AI-Powered Early Warning System for Sudan</p>
</div>
""", unsafe_allow_html=True)
#-----------------------------

#METRICS

#-----------------------------

m1,m2,m3,m4 = st.columns(4)

with m1: st.markdown("<div class='metric-box'><h3>Active Cases</h3><h1>338</h1></div>", unsafe_allow_html=True) with m2: st.markdown("<div class='metric-box'><h3>High Risk Areas</h3><h1>5</h1></div>", unsafe_allow_html=True) with m3: st.markdown("<div class='metric-box'><h3>Alerts</h3><h1>12</h1></div>", unsafe_allow_html=True) with m4: st.markdown("<div class='metric-box'><h3>Model Accuracy</h3><h1>89%</h1></div>", unsafe_allow_html=True)

#-----------------------------

#MAIN LAYOUT

#-----------------------------

col1, col2 = st.columns([2,1])

#-----------------------------

#INTERACTIVE MAP

#-----------------------------

with col1: st.markdown("<div class='glass-card'><h2>🗺 Khartoum Risk Map</h2>", unsafe_allow_html=True)

m = folium.Map(location=[15.55,32.55], zoom_start=8, tiles='cartodbpositron')

districts = [
    ('Khartoum',[15.60,32.53],'Critical','red'),
    ('Omdurman',[15.45,32.40],'High','darkred'),
    ('Bahri',[15.70,32.65],'Medium','orange'),
    ('Karari',[15.75,32.30],'High','darkred'),
    ('East Nile',[15.65,32.75],'Medium','orange'),
    ('Jabal Awliya',[15.20,32.30],'Low','green'),
    ('Sharg Elneel',[15.80,32.80],'Low','green')
]

# Blue Nile
folium.PolyLine([[15.9,32.4],[15.7,32.5],[15.5,32.55]], color='blue', weight=6, tooltip='Blue Nile').add_to(m)

# White Nile
folium.PolyLine([[15.9,32.7],[15.7,32.6],[15.5,32.55]], color='lightblue', weight=6, tooltip='White Nile').add_to(m)

for name,coords,risk,color in districts:
    folium.CircleMarker(
        location=coords,
        radius=18,
        popup=f'{name}<br>Risk Level: {risk}',
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        tooltip=name
    ).add_to(m)

st_folium(m, width=850, height=520)
st.markdown('</div>', unsafe_allow_html=True)

#-----------------------------

#ALERTS PANEL

#-----------------------------

with col2: st.markdown("<div class='glass-card'><h2>🚨 Early Warning</h2>", unsafe_allow_html=True)

alerts = [
    ('critical','Critical outbreak probability in Khartoum','Immediate mosquito control required'),
    ('high','High mosquito activity in Karari','Deploy sanitation teams'),
    ('medium','Rising humidity in Bahri','Increase field monitoring'),
    ('high','Flood risk near Nile banks','Inspect stagnant water zones'),
    ('low','Stable conditions in Jabal Awliya','Continue surveillance')
]

for level,msg,guide in alerts:
    st.markdown(f"<div class='alert-box {level}'><b>{msg}</b><br>{guide}</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

#-----------------------------

#ANALYSIS TABS

#-----------------------------

tab1,tab2,tab3 = st.tabs(['📈 Forecast','🌡 Climate','🔍 SHAP'])

with tab1: st.markdown("<div class='glass-card'>", unsafe_allow_html=True) forecast_df = pd.DataFrame({ 'Week':['W1','W2','W3','W4','W5','W6','W7'], 'Actual':[45,70,120,150,None,None,None], 'Predicted':[50,75,118,155,180,210,245] }) st.line_chart(forecast_df.set_index('Week')) st.caption('Actual dengue cases vs predicted LSTM forecast for next 3 weeks') st.markdown('</div>', unsafe_allow_html=True)

with tab2: st.markdown("<div class='glass-card'>", unsafe_allow_html=True) c1,c2,c3,c4,c5 = st.columns(5) c1.metric('🌡 Temperature','34°C') c2.metric('💧 Humidity','74%') c3.metric('🌧 Rainfall','22mm') c4.metric('🌿 NDVI','0.61') c5.metric('🌊 Flood Risk','High') st.markdown('</div>', unsafe_allow_html=True)

with tab3: st.markdown("<div class='glass-card'>", unsafe_allow_html=True) shap_df = pd.DataFrame({ 'Factor':['Rainfall','Humidity','NDVI','Displacement','Temperature'], 'Importance':[0.42,0.30,0.15,0.09,0.04] }) st.bar_chart(shap_df.set_index('Factor')) st.caption('SHAP explanation for prediction drivers') st.markdown('</div>', unsafe_allow_html=True)

#-----------------------------

#PIPELINE STATUS

#-----------------------------

st.markdown("<div class='glass-card'><h2>⚙ Pipeline Status</h2></div>", unsafe_allow_html=True)

p1,p2,p3,p4 = st.columns(4) p1.success('1️⃣ Ingestion') p2.info('2️⃣ Processing') p3.warning('3️⃣ LSTM Prediction') p4.success('4️⃣ Notifications')

#-----------------------------

#FOOTER

#-----------------------------

st.markdown("""

<hr>
<center>
<p style='color:white;opacity:0.7;'>
DID Prototype v2 | Streamlit + Folium + FastAPI + LSTM Ready
</p>
</center>
""", unsafe_allow_html=True)
