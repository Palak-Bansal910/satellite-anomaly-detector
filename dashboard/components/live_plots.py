# dashboard/components/live_plots.py
import streamlit as st
import plotly.express as px
import pandas as pd

def render_score_trend(df_hist):
    if df_hist.empty:
        st.info("No historical anomaly scores to plot yet.")
        return

    df = df_hist.copy()
    # If timestamp exists and is datetime, use it; else use index.
    if "timestamp" in df.columns and pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        x = df['timestamp']
    else:
        x = df.index

    fig = px.line(df, x=x, y="score", color="satellite_id",
                  title="Anomaly Score over Time",
                  labels={"score": "Score (0-1)", "timestamp": "Time"})
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

def render_issue_distribution(df_hist):
    if df_hist.empty:
        st.info("No issue data to show yet.")
        return

    # explode issues list into rows
    df = df_hist.copy()
    df = df.explode("issues")
    # if issues not present, fill None
    if "issues" not in df.columns:
        st.info("No issue data available.")
        return

    counts = df['issues'].value_counts().reset_index()
    counts.columns = ["issue", "count"]
    fig = px.bar(counts, x="issue", y="count", text="count", title="Issue Frequency (Recent)")
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10), xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
