# ═══════════════════════════════════════════════════════════════════
# DID — Dengue Intelligent Dashboard
# Python + Streamlit Frontend | Phase One Prototype
# Study Area: Khartoum State, Sudan
# Author: Mohammed Badri | 2025
# ═══════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from datetime import datetime

# ─── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="DID · Dengue Intelligent Dashboard",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

.stApp {
    background:
        radial-gradient(ellipse 70% 45% at 8% 0%,  rgba(139,0,0,.38)  0%, transparent 60%),
        radial-gradient(ellipse 55% 40% at 92% 100%,rgba(220,20,60,.20) 0%, transparent 60%),
        #060810 !important;
    font-family: 'Syne', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(220,20,60,.4); border-radius: 2px; }

.did-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(220,20,60,0.18);
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 10px;
    animation: fadeUp .5s ease both;
}

.metric-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(220,20,60,0.18);
    border-radius: 16px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    animation: fadeUp .5s ease both;
    margin-bottom: 10px;
}
.metric-label {
    font-size: 8.5px; letter-spacing: .1em;
    color: rgba(255,255,255,.48); font-family: 'DM Mono', monospace;
    text-transform: uppercase; margin-bottom: 5px;
}
.metric-value {
    font-size: 30px; font-weight: 800; line-height: 1;
    margin-bottom: 4px; font-family: 'Syne', sans-serif;
}
.metric-sub {
    font-size: 9.5px; color: rgba(255,255,255,.28);
}
.metric-bar {
    position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
}

.risk-badge {
    padding: 2px 8px; border-radius: 4px; font-size: 7.5px; font-weight: 700;
    font-family: 'DM Mono', monospace; letter-spacing: .05em;
    display: inline-block; min-width: 60px; text-align: center;
}

.sec-title {
    font-size: 12.5px; font-weight: 700; color: #FFFFFF; margin-bottom: 3px;
}
.sec-sub {
    font-size: 8.5px; color: rgba(255,255,255,.42);
    font-family: 'DM Mono', monospace; margin-bottom: 10px; letter-spacing: .04em;
}

.alert-row {
    display: flex; gap: 10px; align-items: flex-start;
    padding: 9px 0; border-bottom: 1px solid rgba(220,20,60,.13);
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: none; }
}
@keyframes blink {
    0%,100% { opacity: 1; } 50% { opacity: .2; }
}
.live-dot {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: #22C55E; box-shadow: 0 0 8px #22C55E;
    animation: blink 1.6s infinite; vertical-align: middle; margin-right: 5px;
}

div[data-testid="stSidebar"] {
    background: rgba(6,8,16,.96) !important;
    border-right: 1px solid rgba(220,20,60,.2) !important;
}
div[data-testid="stSidebar"] * { color: rgba(255,255,255,.75) !important; }
div[data-testid="stSidebar"] label { font-family: 'Syne', sans-serif !important; font-size: 11px !important; }

div.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(220,20,60,.2) !important;
    gap: 0 !important;
}
div.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(255,255,255,.45) !important;
    font-family: 'Syne', sans-serif !important; font-size: 11px !important;
    border-radius: 0 !important; border-bottom: 2px solid transparent !important;
    padding: 8px 14px !important;
}
div.stTabs [aria-selected="true"] {
    background: rgba(220,20,60,.09) !important;
    color: #DC143C !important;
    border-bottom: 2px solid #DC143C !important;
}
p, li { color: rgba(255,255,255,.75); }
h1,h2,h3 { color: white; font-family: 'Syne', sans-serif; }

div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(220,20,60,.3) !important;
    border-radius: 10px !important;
    color: white !important;
}
div[data-testid="stMultiSelect"] > div {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(220,20,60,.3) !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════

RISK_COLORS = {
    "CRITICAL": "#DC143C",
    "HIGH":     "#E85D04",
    "MEDIUM":   "#F59E0B",
    "LOW":      "#22C55E",
}

DISTRICTS = [
    {
        "id": "karari",    "name": "Karari",      "nameAr": "كرري",
        "risk": "CRITICAL","riskScore": 94,  "cases": 342, "displaced": 12400,
        "temp": 38.2,      "rain": 2.1,
        "color": "#DC143C",
        "coords": [
            [15.72, 32.35],[15.72, 32.53],[15.60, 32.53],
            [15.60, 32.47],[15.58, 32.35],
        ],
    },
    {
        "id": "omdurman",  "name": "Omdurman",    "nameAr": "أم درمان",
        "risk": "HIGH",    "riskScore": 78,  "cases": 289, "displaced": 8900,
        "temp": 37.8,      "rain": 1.8,
        "color": "#E85D04",
        "coords": [
            [15.60, 32.35],[15.60, 32.47],[15.56, 32.48],
            [15.42, 32.48],[15.42, 32.35],
        ],
    },
    {
        "id": "bahri",     "name": "Bahri",        "nameAr": "بحري",
        "risk": "MEDIUM",  "riskScore": 52,  "cases": 124, "displaced": 3200,
        "temp": 37.1,      "rain": 2.4,
        "color": "#F59E0B",
        "coords": [
            [15.72, 32.53],[15.72, 32.68],[15.60, 32.68],
            [15.60, 32.55],[15.61, 32.53],
        ],
    },
    {
        "id": "khartoum",  "name": "Khartoum",    "nameAr": "الخرطوم",
        "risk": "HIGH",    "riskScore": 71,  "cases": 198, "displaced": 5600,
        "temp": 37.5,      "rain": 1.9,
        "color": "#E85D04",
        "coords": [
            [15.60, 32.55],[15.60, 32.68],[15.45, 32.68],
            [15.45, 32.55],[15.56, 32.53],
        ],
    },
    {
        "id": "east_nile", "name": "East Nile",   "nameAr": "شرق النيل",
        "risk": "MEDIUM",  "riskScore": 45,  "cases": 87,  "displaced": 2100,
        "temp": 36.9,      "rain": 2.6,
        "color": "#F59E0B",
        "coords": [
            [15.72, 32.68],[15.72, 32.78],[15.42, 32.78],[15.42, 32.68],
        ],
    },
    {
        "id": "jebel",     "name": "Jebel Aulia", "nameAr": "جبل أولياء",
        "risk": "LOW",     "riskScore": 28,  "cases": 43,  "displaced": 1800,
        "temp": 36.5,      "rain": 3.1,
        "color": "#22C55E",
        "coords": [
            [15.42, 32.35],[15.42, 32.55],[15.32, 32.55],[15.32, 32.35],
        ],
    },
    {
        "id": "soba",      "name": "Soba",         "nameAr": "صوبا",
        "risk": "LOW",     "riskScore": 19,  "cases": 31,  "displaced": 900,
        "temp": 36.2,      "rain": 2.8,
        "color": "#22C55E",
        "coords": [
            [15.42, 32.55],[15.42, 32.78],[15.32, 32.78],[15.32, 32.55],
        ],
    },
]

df_districts = pd.DataFrame([{
    "District":    d["name"],
    "Arabic":      d["nameAr"],
    "Risk Level":  d["risk"],
    "Risk Score":  d["riskScore"],
    "Active Cases":d["cases"],
    "Displaced":   d["displaced"],
    "Temp (°C)":   d["temp"],
    "Rain (mm/wk)":d["rain"],
} for d in DISTRICTS]).sort_values("Risk Score", ascending=False).reset_index(drop=True)

forecast_df = pd.DataFrame([
    {"Week":"Wk-6","Actual":89,  "Predicted":85,  "Phase":"historical"},
    {"Week":"Wk-5","Actual":112, "Predicted":118, "Phase":"historical"},
    {"Week":"Wk-4","Actual":145, "Predicted":142, "Phase":"historical"},
    {"Week":"Wk-3","Actual":178, "Predicted":180, "Phase":"historical"},
    {"Week":"Wk-2","Actual":198, "Predicted":195, "Phase":"historical"},
    {"Week":"Wk-1","Actual":234, "Predicted":228, "Phase":"historical"},
    {"Week":"Now", "Actual":267, "Predicted":271, "Phase":"current"},
    {"Week":"Wk+1","Actual":None,"Predicted":312, "Phase":"forecast"},
    {"Week":"Wk+2","Actual":None,"Predicted":358, "Phase":"forecast"},
    {"Week":"Wk+3","Actual":None,"Predicted":401, "Phase":"forecast"},
])

climate_df = pd.DataFrame([
    {"Indicator":"Temperature","Value":38.2,"Max":50, "Unit":"°C","Icon":"🌡️","Color":"#DC143C"},
    {"Indicator":"Humidity",   "Value":64,  "Max":100,"Unit":"%", "Icon":"💧","Color":"#3B82F6"},
    {"Indicator":"Rainfall",   "Value":28,  "Max":100,"Unit":"mm","Icon":"🌧️","Color":"#60A5FA"},
    {"Indicator":"NDVI Index", "Value":47,  "Max":100,"Unit":"%", "Icon":"🌿","Color":"#22C55E"},
    {"Indicator":"Flood Risk", "Value":72,  "Max":100,"Unit":"%", "Icon":"🌊","Color":"#F59E0B"},
])

shap_df = pd.DataFrame([
    {"Factor":"Rainfall lag (2 weeks)", "Importance":0.82},
    {"Factor":"Displacement density",   "Importance":0.74},
    {"Factor":"NDVI vegetation change", "Importance":0.61},
    {"Factor":"Temperature trend",      "Importance":0.48},
    {"Factor":"Flood extent delta",     "Importance":0.39},
])

ALERTS = [
    {"district":"Karari",    "level":"CRITICAL","msg":"Critical outbreak risk — deploy vector control teams immediately",  "time":"2 hrs ago"},
    {"district":"Omdurman",  "level":"HIGH",    "msg":"High stagnant water density detected post-rainfall event",         "time":"5 hrs ago"},
    {"district":"Khartoum",  "level":"HIGH",    "msg":"Displacement camp density exceeds outbreak threshold (>5,000)",    "time":"8 hrs ago"},
    {"district":"Bahri",     "level":"MEDIUM",  "msg":"Temperature-humidity index rising — intensify surveillance",       "time":"12 hrs ago"},
    {"district":"East Nile", "level":"MEDIUM",  "msg":"NDVI increase signals breeding habitat expansion near Nile banks", "time":"1 day ago"},
]


# ═══════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════

def risk_badge(level: str) -> str:
    c = RISK_COLORS.get(level, "#888")
    return (f'<span class="risk-badge" style="color:{c};'
            f'background:{c}22;border:1px solid {c}50;">{level}</span>')


def metric_card(label: str, value: str, sub: str, color: str) -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color};">{value}</div>
        <div class="metric-sub">{sub}</div>
        <div class="metric-bar"
             style="background:linear-gradient(90deg,{color},transparent);"></div>
    </div>
    """


def build_folium_map(focus_id=None):
    m = folium.Map(
        location=[15.54, 32.56],
        zoom_start=11,
        tiles=None,
        scrollWheelZoom=True,
    )
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://carto.com/">CARTO</a>',
        name="Dark",
        max_zoom=19,
    ).add_to(m)

    for d in DISTRICTS:
        coords   = d["coords"] + [d["coords"][0]]
        is_focus = (focus_id == d["id"])
        fill_op  = 0.85 if is_focus else 0.58
        weight   = 3   if is_focus else 1.2

        popup_html = f"""
        <div style="font-family:Syne,sans-serif;background:#0A0A14;
                    color:#fff;border:1.5px solid {d['color']};
                    border-radius:10px;padding:12px;min-width:190px;">
            <div style="font-weight:800;font-size:13px;margin-bottom:3px;">
                {d['name']}
                <span style="font-size:10px;color:rgba(255,255,255,.5);margin-left:4px;">
                    {d['nameAr']}</span>
            </div>
            <div style="color:{d['color']};font-size:9px;font-weight:700;
                        font-family:'DM Mono',monospace;letter-spacing:.07em;
                        margin-bottom:7px;">{d['risk']} · {d['riskScore']}% RISK</div>
            <hr style="border-color:{d['color']}33;margin:6px 0;"/>
            <table style="font-size:10.5px;width:100%;border-collapse:collapse;">
                <tr><td style="color:rgba(255,255,255,.5);padding:2px 0;">Active Cases</td>
                    <td style="text-align:right;font-weight:700;">{d['cases']:,}</td></tr>
                <tr><td style="color:rgba(255,255,255,.5);">Displaced</td>
                    <td style="text-align:right;color:#F59E0B;font-weight:700;">{d['displaced']:,}</td></tr>
                <tr><td style="color:rgba(255,255,255,.5);">Temperature</td>
                    <td style="text-align:right;color:#FF6B35;font-weight:700;">{d['temp']}°C</td></tr>
                <tr><td style="color:rgba(255,255,255,.5);">Rainfall</td>
                    <td style="text-align:right;color:#60A5FA;font-weight:700;">{d['rain']} mm/wk</td></tr>
            </table>
        </div>
        """

        folium.Polygon(
            locations=coords,
            color=d["color"],
            weight=weight,
            opacity=0.9,
            fill=True,
            fill_color=d["color"],
            fill_opacity=fill_op,
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=(
                f"<b style='font-family:Syne;font-size:12px;'>{d['name']}</b>"
                f"<span style='font-size:10px;color:rgba(255,255,255,.6);'>"
                f" — {d['risk']} ({d['riskScore']}%)</span>"
            ),
        ).add_to(m)

        lat_c = np.mean([c[0] for c in d["coords"]])
        lon_c = np.mean([c[1] for c in d["coords"]])
        folium.Marker(
            location=[lat_c, lon_c],
            icon=folium.DivIcon(
                html=(
                    f"<div style='font-family:Syne,sans-serif;font-size:10px;"
                    f"font-weight:700;color:white;"
                    f"text-shadow:0 1px 4px rgba(0,0,0,.9);"
                    f"white-space:nowrap;text-align:center;'>"
                    f"{d['name']}<br>"
                    f"<span style='font-size:8px;opacity:.7;font-family:DM Mono,monospace;'>"
                    f"{d['riskScore']}% risk</span></div>"
                ),
                icon_size=(110, 30),
                icon_anchor=(55, 0),
            ),
        ).add_to(m)

    return m


def forecast_chart():
    fig = go.Figure()
    actual = forecast_df.dropna(subset=["Actual"])

    fig.add_trace(go.Scatter(
        x=actual["Week"], y=actual["Actual"],
        name="Actual Cases", mode="lines+markers",
        line=dict(color="#FF6B35", width=2.5),
        marker=dict(size=5, color="#FF6B35"),
        fill="tozeroy", fillcolor="rgba(255,107,53,.12)",
    ))
    fig.add_trace(go.Scatter(
        x=forecast_df["Week"], y=forecast_df["Predicted"],
        name="LSTM Forecast", mode="lines",
        line=dict(color="#DC143C", width=2.5, dash="dot"),
        fill="tozeroy", fillcolor="rgba(220,20,60,.07)",
    ))
    fig.add_vrect(
        x0="Wk+1", x1="Wk+3",
        fillcolor="rgba(220,20,60,.05)", layer="below", line_width=0,
        annotation_text="  Forecast Zone",
        annotation_position="top left",
        annotation_font=dict(color="rgba(220,20,60,.5)", size=9),
    )
    fig.update_layout(
        height=230,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Syne", color="rgba(255,255,255,.55)", size=9),
        margin=dict(l=32, r=10, t=10, b=28),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0,
                    font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="rgba(255,255,255,.05)", zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,.05)", zeroline=False,
                   title=dict(text="Cases / Week", font=dict(size=8))),
        hovermode="x unified",
    )
    return fig


def climate_chart():
    fig = go.Figure(go.Bar(
        x=climate_df["Indicator"],
        y=climate_df["Value"],
        marker=dict(color=climate_df["Color"].tolist(), line_width=0),
        text=climate_df.apply(lambda r: f"{r['Value']}{r['Unit']}", axis=1),
        textposition="outside",
        textfont=dict(size=9, color="rgba(255,255,255,.65)"),
    ))
    fig.update_layout(
        height=160,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Syne", color="rgba(255,255,255,.5)", size=9),
        margin=dict(l=10, r=10, t=22, b=10),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=9)),
        yaxis=dict(gridcolor="rgba(255,255,255,.05)"),
        bargap=0.3,
    )
    fig.update_traces(marker_cornerradius=4)
    return fig


def shap_chart():
    fig = go.Figure(go.Bar(
        x=shap_df["Importance"],
        y=shap_df["Factor"],
        orientation="h",
        marker=dict(
            color=shap_df["Importance"],
            colorscale=[[0, "#8B0000"], [0.5, "#DC143C"], [1, "#FF6B35"]],
            line_width=0,
        ),
        text=shap_df["Importance"].apply(lambda v: f"{v:.2f}"),
        textposition="outside",
        textfont=dict(size=9, color="rgba(255,255,255,.65)"),
    ))
    fig.update_layout(
        height=230,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Syne", color="rgba(255,255,255,.55)", size=9),
        margin=dict(l=10, r=50, t=10, b=16),
        xaxis=dict(gridcolor="rgba(255,255,255,.05)", range=[0, 1.1]),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=9.5)),
    )
    fig.update_traces(marker_cornerradius=3)
    return fig


# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:10px 0 18px;">
        <div style="font-size:34px;margin-bottom:6px;">🦟</div>
        <div style="font-size:15px;font-weight:800;color:white;letter-spacing:-.02em;">
            <span style="color:#DC143C;">D</span>ID
        </div>
        <div style="font-size:7.5px;color:rgba(255,255,255,.4);letter-spacing:.14em;
                    font-family:'DM Mono',monospace;margin-top:2px;">
            DENGUE INTELLIGENT DASHBOARD
        </div>
    </div>
    <hr style="border-color:rgba(220,20,60,.2);margin-bottom:14px;"/>
    <div style="font-size:9px;color:rgba(255,255,255,.38);letter-spacing:.09em;
                font-family:'DM Mono',monospace;margin-bottom:8px;">
        FILTERS &amp; CONTROLS
    </div>
    """, unsafe_allow_html=True)

    selected_district = st.selectbox(
        "🗺 Focus District",
        ["All Districts"] + [d["name"] for d in DISTRICTS],
    )
    risk_filter = st.multiselect(
        "⚠ Risk Level Filter",
        ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        default=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
    )

    st.markdown("""
    <hr style="border-color:rgba(220,20,60,.15);margin:14px 0;"/>
    <div style="font-size:9px;color:rgba(255,255,255,.38);letter-spacing:.09em;
                font-family:'DM Mono',monospace;margin-bottom:8px;">
        DATA PIPELINE STATUS
    </div>
    """, unsafe_allow_html=True)

    for stage, status, color in [
        ("Ingestion",       "✓ OK",       "#22C55E"),
        ("Processing",      "✓ OK",       "#22C55E"),
        ("LSTM Inference",  "⟳ RUNNING",  "#F59E0B"),
        ("Alert Dispatch",  "✓ 23 SENT",  "#22C55E"),
    ]:
        st.markdown(
            f"""<div style="display:flex;justify-content:space-between;
                            align-items:center;padding:5px 0;
                            border-bottom:1px solid rgba(220,20,60,.1);">
                <span style="font-size:9.5px;color:rgba(255,255,255,.6);">{stage}</span>
                <span style="font-size:8px;color:{color};font-family:'DM Mono',monospace;
                             font-weight:700;">{status}</span>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""<hr style="border-color:rgba(220,20,60,.15);margin:14px 0;"/>
        <div style="font-size:7.5px;color:rgba(255,255,255,.22);
                    font-family:'DM Mono',monospace;line-height:1.85;">
            MODEL: LSTM v1.0<br/>
            LAST SYNC: {datetime.now().strftime("%H:%M:%S")}<br/>
            DATA: NASA · CHIRPS · WHO · UNHCR<br/>
            © 2025 MOHAMMED BADRI
        </div>""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════

st.markdown(
    f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
                padding:10px 0 16px;border-bottom:1px solid rgba(220,20,60,.18);
                margin-bottom:18px;flex-wrap:wrap;gap:10px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:40px;height:40px;border-radius:10px;
                        background:linear-gradient(135deg,#DC143C,#8B0000);
                        display:flex;align-items:center;justify-content:center;
                        font-size:20px;box-shadow:0 0 22px rgba(220,20,60,.5);">🦟</div>
            <div>
                <div style="font-size:15px;font-weight:800;color:white;letter-spacing:-.02em;">
                    <span style="color:#DC143C;">D</span>ID — Dengue Intelligent Dashboard
                </div>
                <div style="font-size:8.5px;color:rgba(255,255,255,.4);letter-spacing:.1em;
                            font-family:'DM Mono',monospace;margin-top:1px;">
                    KHARTOUM STATE, SUDAN · LSTM EARLY WARNING SYSTEM · PHASE ONE
                </div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
            <div>
                <span class="live-dot"></span>
                <span style="font-size:10px;color:rgba(255,255,255,.45);
                             font-family:'DM Mono',monospace;">LIVE</span>
            </div>
            <div style="padding:3px 12px;border-radius:20px;font-size:9px;font-weight:700;
                        background:rgba(220,20,60,.14);border:1px solid rgba(220,20,60,.4);
                        color:#FF4455;letter-spacing:.07em;">
                ⚠ OUTBREAK RISK: HIGH
            </div>
            <span style="font-size:9px;color:rgba(255,255,255,.28);
                         font-family:'DM Mono',monospace;">
                {datetime.now().strftime("%d %b %Y · %H:%M")}
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════
# METRIC CARDS
# ═══════════════════════════════════════════════════════

mc1, mc2, mc3, mc4 = st.columns(4, gap="small")

with mc1:
    st.markdown(metric_card("ACTIVE CASES", "1,114",
                "Khartoum State · 2025", "#DC143C"), unsafe_allow_html=True)
with mc2:
    st.markdown(metric_card("HIGH-RISK DISTRICTS", "5",
                "of 7 localities monitored", "#E85D04"), unsafe_allow_html=True)
with mc3:
    st.markdown(metric_card("ACTIVE ALERTS", "23",
                "requiring intervention", "#F59E0B"), unsafe_allow_html=True)
with mc4:
    st.markdown(metric_card("LSTM RECALL SCORE", "91%",
                "≥ 90% WHO sensitivity threshold ✓", "#22C55E"), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# MAIN GRID — MAP + CHARTS
# ═══════════════════════════════════════════════════════

col_map, col_charts = st.columns([1.05, 0.95], gap="medium")

with col_map:
    st.markdown("""
    <div class="sec-title">🗺 Khartoum State — Outbreak Risk Map</div>
    <div class="sec-sub">District-level LSTM prediction · Click any district for full details</div>
    """, unsafe_allow_html=True)

    leg = st.columns(4)
    for i, (lvl, col) in enumerate(RISK_COLORS.items()):
        with leg[i]:
            st.markdown(
                f"""<div style="display:flex;align-items:center;gap:5px;margin-bottom:6px;">
                <div style="width:10px;height:10px;border-radius:3px;background:{col};
                            box-shadow:0 0 5px {col}88;"></div>
                <span style="font-size:8.5px;color:rgba(255,255,255,.5);
                             font-family:'DM Mono',monospace;">{lvl}</span></div>""",
                unsafe_allow_html=True,
            )

    focus_id = None
    if selected_district != "All Districts":
        focus_id = next((d["id"] for d in DISTRICTS
                         if d["name"] == selected_district), None)

    m = build_folium_map(focus_id)
    st_folium(m, width="100%", height=440,
              returned_objects=["last_object_clicked_tooltip"])


with col_charts:
    tab_fore, tab_clim, tab_shap = st.tabs(
        ["📈 Forecast", "🌡️ Climate", "🔍 SHAP"]
    )

    with tab_fore:
        st.markdown(
            '<div style="font-size:9.5px;color:rgba(255,255,255,.45);margin-bottom:4px;">'
            'Weekly cases + LSTM 3-week ahead prediction</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(forecast_chart(), use_container_width=True,
                        config={"displayModeBar": False})

        st.markdown(
            '<div style="font-size:8.5px;color:rgba(255,255,255,.35);'
            'font-family:DM Mono;letter-spacing:.07em;margin:6px 0 5px;">'
            'TOP SHAP DRIVERS — THIS WEEK</div>',
            unsafe_allow_html=True,
        )
        for _, row in shap_df.iterrows():
            pct = int(row["Importance"] * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
                <span style="font-size:9.5px;color:rgba(255,255,255,.62);min-width:162px;">
                    {row['Factor']}</span>
                <div style="flex:1;height:5px;border-radius:3px;
                            background:rgba(255,255,255,.07);">
                    <div style="width:{pct}%;height:100%;border-radius:3px;
                                background:linear-gradient(90deg,#8B0000,#DC143C,#FF6B35);">
                    </div>
                </div>
                <span style="font-size:8.5px;color:#DC143C;font-family:'DM Mono',monospace;
                             font-weight:700;width:28px;text-align:right;">
                    {row['Importance']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)

    with tab_clim:
        st.markdown(
            '<div style="font-size:9.5px;color:rgba(255,255,255,.45);margin-bottom:8px;">'
            'Current satellite & sensor readings — Khartoum State</div>',
            unsafe_allow_html=True,
        )
        for _, row in climate_df.iterrows():
            pct = min(int((row["Value"] / row["Max"]) * 100), 100)
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-size:11px;color:rgba(255,255,255,.78);">
                        {row['Icon']} {row['Indicator']}</span>
                    <span style="font-size:11px;color:{row['Color']};font-weight:700;
                                 font-family:'DM Mono',monospace;">
                        {row['Value']}{row['Unit']}</span>
                </div>
                <div style="height:5px;border-radius:3px;background:rgba(255,255,255,.07);">
                    <div style="width:{pct}%;height:100%;border-radius:3px;
                                background:{row['Color']};opacity:.85;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.plotly_chart(climate_chart(), use_container_width=True,
                        config={"displayModeBar": False})

    with tab_shap:
        st.markdown("""
        <div style="padding:10px 14px;border-radius:10px;
                    background:rgba(220,20,60,.06);border:1px solid rgba(220,20,60,.15);
                    margin-bottom:10px;display:flex;gap:22px;">
            <div>
                <div style="font-size:8.5px;color:rgba(255,255,255,.38);">CONFIDENCE</div>
                <div style="font-size:20px;font-weight:800;color:#22C55E;">91%</div>
            </div>
            <div>
                <div style="font-size:8.5px;color:rgba(255,255,255,.38);">MODEL</div>
                <div style="font-size:20px;font-weight:800;color:#DC143C;">LSTM v1.2</div>
            </div>
            <div>
                <div style="font-size:8.5px;color:rgba(255,255,255,.38);">HORIZON</div>
                <div style="font-size:20px;font-weight:800;color:#F59E0B;">3 Weeks</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(shap_chart(), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown(
            '<div style="font-size:8.5px;color:rgba(255,255,255,.28);line-height:1.7;">'
            'ℹ SHAP values quantify each variable\'s contribution to the outbreak risk score. '
            'Higher values indicate stronger causal influence on the current weekly prediction.</div>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════
# BOTTOM ROW — ALERTS + TABLE
# ═══════════════════════════════════════════════════════

st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
bot_l, bot_r = st.columns([1.2, 1], gap="medium")

with bot_l:
    st.markdown("""
    <div class="sec-title">🚨 Active Alerts & Field Guidance</div>
    <div class="sec-sub">Dispatched to registered health officials via email + SMS</div>
    """, unsafe_allow_html=True)

    filtered_alerts = [a for a in ALERTS if a["level"] in risk_filter]
    alerts_html = ""
    for a in filtered_alerts:
        alerts_html += f"""
        <div class="alert-row">
            <div style="padding-top:1px;">{risk_badge(a['level'])}</div>
            <div style="flex:1;">
                <div style="font-size:10.5px;font-weight:600;color:white;
                            margin-bottom:2px;">{a['district']}</div>
                <div style="font-size:9.5px;color:rgba(255,255,255,.52);
                            line-height:1.45;">{a['msg']}</div>
            </div>
            <div style="font-size:8.5px;color:rgba(255,255,255,.25);
                        white-space:nowrap;padding-top:1px;">{a['time']}</div>
        </div>
        """
    st.markdown(
        f'<div class="did-card" style="padding:10px 16px;">{alerts_html}</div>',
        unsafe_allow_html=True,
    )

with bot_r:
    st.markdown("""
    <div class="sec-title">📊 District Risk Summary</div>
    <div class="sec-sub">Sorted by risk score · Filtered by sidebar selection</div>
    """, unsafe_allow_html=True)

    df_show = df_districts[df_districts["Risk Level"].isin(risk_filter)].copy()
    rows_html = ""
    for _, row in df_show.iterrows():
        color = RISK_COLORS.get(row["Risk Level"], "#888")
        pct   = int(row["Risk Score"])
        rows_html += f"""
        <tr style="border-top:1px solid rgba(220,20,60,.1);">
            <td style="padding:9px 12px;font-weight:600;color:white;font-size:10px;">
                {row['District']}</td>
            <td style="padding:9px 10px;">
                <span style="padding:2px 7px;border-radius:3px;font-size:7.5px;
                             font-weight:700;background:{color}22;color:{color};
                             border:1px solid {color}44;font-family:'DM Mono',monospace;">
                    {row['Risk Level']}</span></td>
            <td style="padding:9px 10px;font-family:'DM Mono',monospace;
                       color:rgba(255,255,255,.78);font-size:10px;">{row['Active Cases']}</td>
            <td style="padding:9px 10px;min-width:110px;">
                <div style="display:flex;align-items:center;gap:6px;">
                    <div style="flex:1;height:5px;border-radius:3px;
                                background:rgba(255,255,255,.08);">
                        <div style="width:{pct}%;height:100%;border-radius:3px;
                                    background:{color};"></div>
                    </div>
                    <span style="color:{color};font-family:'DM Mono',monospace;
                                 font-size:8.5px;font-weight:700;width:30px;
                                 text-align:right;">{pct}%</span>
                </div>
            </td>
        </tr>
        """

    st.markdown(f"""
    <div class="did-card" style="padding:0;overflow:hidden;">
    <table style="width:100%;border-collapse:collapse;">
        <thead>
            <tr style="background:rgba(255,255,255,.03);">
                <th style="padding:8px 12px;text-align:left;color:rgba(255,255,255,.4);
                           font-weight:600;letter-spacing:.07em;font-size:8px;">DISTRICT</th>
                <th style="padding:8px 10px;text-align:left;color:rgba(255,255,255,.4);
                           font-weight:600;letter-spacing:.07em;font-size:8px;">RISK</th>
                <th style="padding:8px 10px;text-align:left;color:rgba(255,255,255,.4);
                           font-weight:600;letter-spacing:.07em;font-size:8px;">CASES</th>
                <th style="padding:8px 10px;text-align:left;color:rgba(255,255,255,.4);
                           font-weight:600;letter-spacing:.07em;font-size:8px;">SCORE</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════

st.markdown(
    f"""
    <div style="text-align:center;padding:20px 0 10px;
                color:rgba(255,255,255,.2);font-size:8px;
                font-family:'DM Mono',monospace;line-height:1.9;margin-top:12px;
                border-top:1px solid rgba(220,20,60,.12);">
        DID — DENGUE INTELLIGENT DASHBOARD · KHARTOUM STATE, SUDAN<br/>
        DATA SOURCES: NASA POWER · CHIRPS · ERA5 · MODIS NDVI · WHO EMRO · UNHCR IDP TRACKER<br/>
        ALGORITHM: LSTM TIME-SERIES DEEP LEARNING · BASELINE: ARIMA + RANDOM FOREST<br/>
        PHASE ONE PROTOTYPE · © 2025 MOHAMMED BADRI — ALL RIGHTS RESERVED
    </div>
    """,
    unsafe_allow_html=True,
)
