import streamlit as st
import requests


BACKEND_URL = st.secrets.get('BACKEND_URL', 'http://backend:8000')


st.title('SkyHack — Anomaly Dashboard')


resp = requests.get(f"{BACKEND_URL}/anomalies?limit=50")
if resp.status_code == 200:
data = resp.json()
if not data:
st.info('No anomalies yet')
else:
for a in data:
st.write(f"{a['timestamp']} — {a['satellite_id']} — {a['metric']} = {a['value']} ({a['severity']})")
else:
st.error('Could not reach backend')
