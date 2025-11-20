# dashboard/components/health_panel.py
import streamlit as st
import pandas as pd

def render_health_panel(df_hist, latest):
    total = len(df_hist)
    critical = 0
    warning = 0
    normal = 0
    if not df_hist.empty:
        counts = df_hist['severity'].value_counts().to_dict()
        critical = counts.get('critical', 0)
        warning = counts.get('warning', 0)
        normal = counts.get('normal', 0)

    latest_sev = "N/A"
    if latest:
        latest_sev = latest[0].get('anomaly', {}).get('severity', 'N/A')

    st.metric("Latest Severity", latest_sev)
    st.metric("Total anomalies logged", total)

    st.write("Severity breakdown")
    col1, col2, col3 = st.columns(3)
    col1.metric("Critical", critical)
    col2.metric("Warning", warning)
    col3.metric("Normal", normal)

    st.write("---")
    st.write("Quick checks")
    st.write("- Backend: `http://127.0.0.1:8000`")
    st.write("- Anomalies endpoint: `/anomalies/latest`")
    st.write("- History endpoint: `/anomalies/history?limit=50`")
