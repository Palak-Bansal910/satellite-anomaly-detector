import streamlit as st
import requests
import pandas as pd

API_LATEST = "http://localhost:8000/anomalies/latest"
API_HISTORY = "http://localhost:8000/anomalies/history"

st.set_page_config(layout="wide", page_title="Satellite Anomaly Dashboard")

STATUS_COLORS = {
    "normal": "🟢",
    "warning": "🟡",
    "critical": "🔴"
}

def fetch(url):
    try:
        r = requests.get(url)
        return r.json()
    except:
        return []

view = st.sidebar.radio("Choose View", ["Live", "History"])

if view == "Live":
    data = fetch(API_LATEST)
else:
    data = fetch(API_HISTORY)

df = pd.DataFrame(data)

left, right = st.columns([2, 1])

with left:
    st.subheader(f"{view} Anomalies")
    if df.empty:
        st.info("No anomaly data available.")
    else:
        df_display = df.copy()
        df_display["level"] = df_display["level"].apply(lambda x: f"{STATUS_COLORS.get(x, '⚪')}  {x}")
        st.dataframe(df_display, hide_index=True, use_container_width=True)

with right:
    st.subheader("Satellite Health Summary")
    st.metric("Active Alerts", len(df))

    if not df.empty:
        st.write(f"**Latest Status:** {STATUS_COLORS.get(df.iloc[-1]['level'], '')} {df.iloc[-1]['level']}")

    st.write("---")
    st.subheader("Anomaly Score Trend")

    hist = fetch(API_HISTORY)
    if hist:
        hist_df = pd.DataFrame(hist)
        if "score" in hist_df.columns:
            st.line_chart(hist_df[["score"]])
        else:
            st.info("No score field found")
    else:
        st.info("History endpoint unavailable.")
