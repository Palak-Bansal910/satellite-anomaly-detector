# backend/api/routes/alerts.py
import os
import json
import requests
import smtplib
from email.message import EmailMessage
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()  # reads .env in project root

router = APIRouter(tags=["Alerts"])

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")  # set in .env
EMAIL_HOST = os.getenv("ALERT_EMAIL_HOST")     # smtp host
EMAIL_PORT = int(os.getenv("ALERT_EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("ALERT_EMAIL_USER")
EMAIL_PASS = os.getenv("ALERT_EMAIL_PASS")
EMAIL_TO = os.getenv("ALERT_EMAIL_TO")         # comma separated list

class AlertRequest(BaseModel):
    timestamp: str
    satellite_id: str
    severity: str
    issues: list[str]
    score: float

@router.post("/send")
def send_alert(payload: AlertRequest):
    summary = f"ALERT | {payload.satellite_id} | {payload.severity.upper()} | Issues: {', '.join(payload.issues)} | Score: {payload.score}"
    result = {"slack": False, "email": False, "errors": []}

    # Slack
    if SLACK_WEBHOOK:
        try:
            slack_payload = {"text": summary + f"\nTimestamp: {payload.timestamp}"}
            resp = requests.post(SLACK_WEBHOOK, json=slack_payload, timeout=5)
            resp.raise_for_status()
            result["slack"] = True
        except Exception as e:
            result["errors"].append(f"slack:{str(e)}")

    # Email
    if EMAIL_HOST and EMAIL_USER and EMAIL_PASS and EMAIL_TO:
        try:
            msg = EmailMessage()
            msg["Subject"] = f"[Satellite Alert] {payload.satellite_id} - {payload.severity.upper()}"
            msg["From"] = EMAIL_USER
            msg["To"] = [x.strip() for x in EMAIL_TO.split(",")]
            msg.set_content(summary + f"\nTimestamp: {payload.timestamp}\n\nDetails: {json.dumps(payload.dict(), indent=2)}")

            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=10) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)
            result["email"] = True
        except Exception as e:
            result["errors"].append(f"email:{str(e)}")

    if not (result["slack"] or result["email"]):
        if not SLACK_WEBHOOK and not (EMAIL_HOST and EMAIL_USER and EMAIL_PASS and EMAIL_TO):
            raise HTTPException(
                status_code=503,
                detail={
                    "msg": "Alert service not configured. Please configure Slack webhook or Email settings in .env file",
                    "result": result,
                    "config_required": True
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "msg": "Failed to send alerts through configured channels",
                    "result": result,
                    "config_required": False
                }
            )

    return {"status": "sent", **result}
