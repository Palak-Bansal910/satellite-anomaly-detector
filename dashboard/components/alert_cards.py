# dashboard/components/alert_cards.py
import streamlit as st
from datetime import datetime
import requests

BACKEND_ALERT_URL = "http://127.0.0.1:8000/alerts/send"

SEVERITY_COLORS = {
    "normal": "#2ECC71",
    "warning": "#F1C40F",
    "critical": "#E74C3C"
}

def _pretty_issues(issues):
    if not issues:
        return "None"
    if isinstance(issues, list):
        return ", ".join(issues)
    return str(issues)

def _format_ts(ts):
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts

def send_alert_to_backend(item):
    # build payload
    ann = item.get("anomaly", {})
    payload = {
        "timestamp": item.get("timestamp"),
        "satellite_id": item.get("satellite_id"),
        "severity": ann.get("severity", "normal"),
        "issues": ann.get("issues", []),
        "score": ann.get("score", 0.0)
    }
    try:
        resp = requests.post(BACKEND_ALERT_URL, json=payload, timeout=5)
        if resp.ok:
            return {"ok": True, "result": resp.json()}
        return {"ok": False, "result": resp.text}
    except Exception as e:
        return {"ok": False, "result": str(e)}

def render_alert_card(item, show_send_button=True):
    ann = item.get("anomaly", {})
    severity = ann.get("severity", "normal")
    color = SEVERITY_COLORS.get(severity, "#95A5A6")
    ts = _format_ts(item.get("timestamp", ""))

    container = st.container()
    with container:
        cols = st.columns([3,1])
        with cols[0]:
            st.markdown(
                f"""
                <div style="border-left:6px solid {color}; padding:10px; margin-bottom:8px; background:#F8F9F9; border-radius:6px;">
                <strong>Satellite:</strong> {item.get('satellite_id', 'unknown')} &nbsp;&nbsp; <small>{ts}</small><br>
                <strong>Severity:</strong> <span style="color:{color}; font-weight:700">{severity.upper()}</span><br>
                <strong>Issues:</strong> {_pretty_issues(ann.get('issues', []))} <br>
                <strong>Score:</strong> {round(ann.get('score', 0.0), 2)}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with cols[1]:
            # send alert button and status placeholder
            if show_send_button:
                btn_key = f"send_{item.get('timestamp')}_{item.get('satellite_id')}"
                if st.button("📣 Send Alert", key=btn_key):
                    with st.spinner("Sending alert..."):
                        resp = send_alert_to_backend(item)
                    if resp["ok"]:
                        st.success("Sent ✅")
                        # optionally show channels
                        res = resp.get("result", {})
                        st.write(res)
                    else:
                        st.error("Failed to send")
                        st.write(resp.get("result"))
            else:
                st.write("")
