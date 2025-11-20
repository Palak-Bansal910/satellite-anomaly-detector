# dashboard/streamlit_app.py
import time
import requests
import pandas as pd
import streamlit as st

from components.alert_cards import render_alert_card
from components.health_panel import render_health_panel
from components.live_plots import render_score_trend, render_issue_distribution
from components.orbit_visualizer import render_orbit_visualizer

BASE_URL = "http://127.0.0.1:8000"
LATEST_ENDPOINT = f"{BASE_URL}/anomalies/latest"
HISTORY_ENDPOINT = f"{BASE_URL}/anomalies/history?limit=500"

st.set_page_config(page_title="🛰 Satellite Anomaly Detector", layout="wide")

st.title("🛰 Satellite Anomaly Detector — Mission Dashboard")
st.markdown("Live telemetry → anomaly pipeline. Use controls on the right to filter/playback.")

# fetch functions
@st.cache_data(ttl=3)
def fetch_latest():
    try:
        r = requests.get(LATEST_ENDPOINT, timeout=2)
        return r.json().get("data", []) if r.ok else []
    except Exception:
        return []

@st.cache_data(ttl=5)
def fetch_history():
    try:
        r = requests.get(HISTORY_ENDPOINT, timeout=4)
        data = r.json().get("data", []) if r.ok else []
        # normalize issues as lists
        for item in data:
            if isinstance(item.get("issues"), str):
                item["issues"] = item["issues"].split(",") if item["issues"] else []
        return data
    except Exception:
        return []

latest = fetch_latest()
history = fetch_history()

# build dataframe for UI controls
df_hist = pd.DataFrame(history)
if not df_hist.empty:
    try:
        df_hist["timestamp"] = pd.to_datetime(df_hist["timestamp"])
    except Exception:
        pass
else:
    df_hist = pd.DataFrame(columns=["timestamp", "satellite_id", "severity", "issues", "score"])

# RIGHT: control panel
with st.sidebar:
    st.header("Controls")
    sats = sorted(df_hist['satellite_id'].unique().tolist()) if not df_hist.empty else []
    selected_sat = st.selectbox("Filter satellite", options=["All"] + sats)
    play_toggle = st.checkbox("Play animation", value=False)
    # slider for manual frame selection
    timestamps = sorted(df_hist['timestamp'].unique().tolist()) if not df_hist.empty else []
    if timestamps:
        slider_index = st.slider("Playback frame", 0, max(0, len(timestamps)-1), 0)
    else:
        slider_index = 0
    st.markdown("---")
    st.write("Auto-refresh every ~4 seconds")

# MAIN layout
col1, col2 = st.columns([3,1])

with col1:
    st.subheader("Live Alerts")
    if not latest:
        st.info("No anomalies yet...")
    else:
        # apply satellite filter to latest
        if selected_sat != "All":
            latest_filtered = [l for l in latest if l.get("satellite_id") == selected_sat]
        else:
            latest_filtered = latest
        
        for item in latest_filtered:
            render_alert_card(item)

    st.markdown("---")
    st.subheader("Anomaly Score Trend")
    render_score_trend(df_hist)

    st.markdown("---")
    st.subheader("Issue Frequency (Recent)")
    render_issue_distribution(df_hist)

    st.markdown("---")
    st.subheader("Orbit Visualizer")
    # pass selected_sat to visualizer; play toggle and slider index control view
    sel_sat = None if selected_sat == "All" else selected_sat
    render_orbit_visualizer(history, selected_satellite=sel_sat, play=play_toggle, slider_index=slider_index)

with col2:
    st.subheader("System Health")
    render_health_panel(df_hist, latest)
    st.markdown("---")
    st.write("Demo tips:")
    st.write("- Start backend (uvicorn api.main:app --reload)")
    st.write("- Start simulator to stream telemetry")
    st.write("- Use Slack/email config in .env to enable push alerts")
