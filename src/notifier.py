"""
notifier.py — Slack + Email notification module (Gmail API OAuth 2.0)
Gửi thông báo real-time cho từng job SUCCESS/FAILURE.
"""
import os
import logging
import base64
import json
import mimetypes
from email.message import EmailMessage
from typing import Optional

import requests
from dotenv import load_dotenv

# OAuth 2.0 imports
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

load_dotenv()
logger = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
EMAIL_ADMIN       = os.getenv("EMAIL_ADMIN")

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# ─── Slack ────────────────────────────────────────────────────────────────────

def _send_slack(blocks: list) -> bool:
    """Gửi Slack block message qua webhook."""
    if not SLACK_WEBHOOK_URL or SLACK_WEBHOOK_URL.startswith("https://hooks.slack.com/services/YOUR"):
        logger.debug("[SLACK] Webhook not configured — skipping")
        return False
    try:
        resp = requests.post(
            SLACK_WEBHOOK_URL,
            data=json.dumps({"blocks": blocks}),
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if resp.status_code != 200:
            logger.warning(f"[SLACK] Non-200 response: {resp.status_code} — {resp.text}")
            return False
        return True
    except Exception as e:
        logger.error(f"[SLACK] Send failed: {e}")
        return False


# ─── Email (Gmail API OAuth 2.0) ───────────────────────────────────────────────

def _get_gmail_service():
    """Lấy Service qua OAuth 2.0 thay vì SMTP App Password."""
    creds = None
    if os.path.exists("gmail_token.json"):
        creds = Credentials.from_authorized_user_file("gmail_token.json", GMAIL_SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_secret_path = os.getenv("GOOGLE_OAUTH_CLIENT_JSON", "client_secret.json")
            if not os.path.exists(client_secret_path):
                logger.debug(f"[EMAIL] Missing {client_secret_path} for Gmail OAuth — skipping email.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open("gmail_token.json", "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def _send_email(subject: str, html_body: str, to: Optional[str] = None, attachment_path: Optional[str] = None) -> bool:
    """Gửi HTML email qua Gmail API, hỗ trợ gửi kèm file."""
    to = to or EMAIL_ADMIN
    if not to:
        logger.debug("[EMAIL] EMAIL_ADMIN not configured — skipping")
        return False

    service = _get_gmail_service()
    if not service:
        return False

    try:
        message = EmailMessage()
        message.set_content("Please enable HTML to view this message.")
        message.add_alternative(html_body, subtype="html")
        message["To"] = to
        message["Subject"] = subject
        
        if attachment_path and os.path.exists(attachment_path):
            ctype, encoding = mimetypes.guess_type(attachment_path)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)
            with open(attachment_path, "rb") as fp:
                message.add_attachment(fp.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(attachment_path))
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        
        service.users().messages().send(userId="me", body=create_message).execute()
        logger.info(f"[EMAIL] Sent via Gmail API to {to}: {subject}")
        return True
    except Exception as e:
        logger.error(f"[EMAIL] Send failed: {e}")
        return False


# ─── Public API ───────────────────────────────────────────────────────────────

def notify_success(job_id: int, description: str, drive_url: str,
                   model_used: str, duration_ms: int):
    """Gửi thông báo SUCCESS qua Slack + Email."""
    emoji = "✅"
    title = f"{emoji} Asset Generated — Job #{job_id:04d}"

    # Slack blocks
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": title, "emoji": True}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*Description:*\n{description[:80]}"},
            {"type": "mrkdwn", "text": f"*Model:* {model_used}"},
            {"type": "mrkdwn", "text": f"*Duration:* {duration_ms}ms"},
            {"type": "mrkdwn", "text": f"*Drive URL:*\n<{drive_url}|View Asset>"},
        ]},
        {"type": "divider"},
    ]
    _send_slack(blocks)

    # Email
    html = f"""
    <h2 style="color:#27ae60;">{title}</h2>
    <p><b>Job ID:</b> {job_id}</p>
    <p><b>Description:</b> {description}</p>
    <p><b>Model Used:</b> {model_used}</p>
    <p><b>Execution Time:</b> {duration_ms}ms</p>
    <p><b>Asset URL:</b> <a href="{drive_url}">{drive_url}</a></p>
    """
    _send_email(title, html)


def notify_failure(job_id: int, description: str, error: str,
                   retry_count: int, output_format: str):
    """Gửi thông báo FAILURE qua Slack + Email."""
    emoji = "❌"
    title = f"{emoji} Asset Failed — Job #{job_id:04d}"

    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": title, "emoji": True}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*Description:*\n{description[:80]}"},
            {"type": "mrkdwn", "text": f"*Format:* {output_format}"},
            {"type": "mrkdwn", "text": f"*Retries:* {retry_count}"},
            {"type": "mrkdwn", "text": f"*Error:*\n```{error[:200]}```"},
        ]},
        {"type": "divider"},
    ]
    _send_slack(blocks)

    html = f"""
    <h2 style="color:#e74c3c;">{title}</h2>
    <p><b>Job ID:</b> {job_id}</p>
    <p><b>Description:</b> {description}</p>
    <p><b>Format:</b> {output_format}</p>
    <p><b>Retries Exhausted:</b> {retry_count}</p>
    <p><b>Error:</b> <code style="color:red">{error}</code></p>
    """
    _send_email(title, html)


def notify_daily_report(report_path: str, stats: dict):
    """Gửi daily report summary qua Email."""
    title = f"📊 Daily Report — {stats.get('date', 'Today')}"
    html = f"""
    <h2>{title}</h2>
    <table border="1" cellpadding="8" style="border-collapse:collapse;">
      <tr><th>Metric</th><th>Value</th></tr>
      <tr><td>Total Jobs</td><td>{stats.get('total', 0)}</td></tr>
      <tr><td>Success</td><td style="color:green"><b>{stats.get('success', 0)}</b></td></tr>
      <tr><td>Failed</td><td style="color:red"><b>{stats.get('failed', 0)}</b></td></tr>
      <tr><td>Success Rate</td><td><b>{stats.get('success_rate', 0)}%</b></td></tr>
      <tr><td>Avg Execution Time</td><td>{stats.get('avg_exec_ms', 0)}ms</td></tr>
    </table>
    <p><i>Full HTML report is attached to this email.</i></p>
    """
    _send_email(title, html, attachment_path=report_path)
    logger.info(f"[NOTIFIER] Daily report sent for {stats.get('date')}")
