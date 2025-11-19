import time
import requests
import random


BACKEND = "http://localhost:8000/anomalies"


sat_ids = ['SAT-A', 'SAT-B', 'SAT-C']
metrics = ['temperature', 'battery', 'signal']


if __name__ == '__main__':
while True:
payload = {
'satellite_id': random.choice(sat_ids),
'metric': random.choice(metrics),
'value': round(random.uniform(0, 100), 2),
'severity': random.choice(['low','medium','high'])
}
try:
r = requests.post(BACKEND, json=payload, timeout=3)
print('sent', payload, '=>', r.status_code)
except Exception as e:
print('error', e)
time.sleep(3)
