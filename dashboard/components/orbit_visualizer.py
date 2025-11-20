# dashboard/components/orbit_visualizer.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def build_frames(df, sat_list):
    # df must have columns: timestamp (datetime), satellite_id, position_x, position_y
    frames = []
    timestamps = sorted(df['timestamp'].unique())
    for t in timestamps:
        sub = df[df['timestamp'] == t]
        data = []
        for sat in sat_list:
            sat_sub = sub[sub['satellite_id'] == sat]
            if not sat_sub.empty:
                data.append(go.Scatter(x=sat_sub['position_x'], y=sat_sub['position_y'],
                                       mode='markers',
                                       marker=dict(size=8),
                                       name=sat))
        frames.append(go.Frame(data=data, name=str(t)))
    return frames, timestamps

def render_orbit_visualizer(history_records, selected_satellite=None, play=False, slider_index=0):
    # assemble DataFrame with positions
    rows = []
    for r in history_records:
        # backend may include pos fields; check keys robustly
        px = r.get("position_x") or r.get("pos_x") or r.get("x")
        py = r.get("position_y") or r.get("pos_y") or r.get("y")
        if px is None or py is None:
            continue
        try:
            rows.append({
                "timestamp": pd.to_datetime(r.get("timestamp")),
                "satellite_id": r.get("satellite_id") or "SAT-UNK",
                "position_x": float(px),
                "position_y": float(py)
            })
        except Exception:
            continue

    if len(rows) == 0:
        st.info("Position data unavailable from backend. Showing placeholder image.")
        st.image("/mnt/data/d95c7e05-7a68-4857-bc74-e64108d8518e.png", caption="Orbit placeholder", use_column_width=True)
        return

    df = pd.DataFrame(rows)
    df = df.sort_values("timestamp")
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # satellite selector
    sat_list = sorted(df['satellite_id'].unique())
    selected = selected_satellite if selected_satellite in sat_list else sat_list

    # prepare frames
    frames, timestamps = build_frames(df, sat_list)

    # base figure with first timestamp
    first_t = timestamps[0]
    first_df = df[df['timestamp'] == first_t]

    fig = go.Figure()

    for sat in sat_list:
        sat_df = first_df[first_df['satellite_id'] == sat]
        fig.add_trace(go.Scatter(
            x=sat_df['position_x'],
            y=sat_df['position_y'],
            mode='markers',
            marker=dict(size=8),
            name=sat
        ))

    # layout + frames
    fig.update_layout(
        xaxis=dict(title="X (km)"),
        yaxis=dict(title="Y (km)"),
        title=f"Orbit positions over time (frames: {len(timestamps)})",
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            y=1,
            x=1.12,
            xanchor="right",
            yanchor="top",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None, {"frame": {"duration": 400, "redraw": True},
                                       "fromcurrent": True, "transition": {"duration": 200}}])]
        )]
    )

    fig.frames = frames

    # show slider if requested
    if not play:
        # render static at slider_index
        ts = timestamps[slider_index]
        sub = df[df['timestamp'] == ts]
        fig2 = go.Figure()
        for sat in sat_list:
            sat_sub = sub[sub['satellite_id'] == sat]
            if selected_satellite and sat != selected_satellite:
                continue
            fig2.add_trace(go.Scatter(x=sat_sub['position_x'], y=sat_sub['position_y'], mode='markers', name=sat))
        fig2.update_layout(title=f"Positions at {ts}", xaxis_title="X (km)", yaxis_title="Y (km)", height=450)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.plotly_chart(fig, use_container_width=True)
