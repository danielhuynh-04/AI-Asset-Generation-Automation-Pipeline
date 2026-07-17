"""
notifier.py — Slack + Email notification module
Gửi thông báo real-time cho từng job SUCCESS/FAILURE.
"""
import os
import logging
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SMTP_HOST         = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT         = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER         = os.getenv("SMTP_USER")
SMTP_PASSWORD     = os.getenv("SMTP_PASSWORD")
EMAIL_ADMIN       = os.getenv("EMAIL_ADMIN")


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


# ─── Email ────────────────────────────────────────────────────────────────────

def _send_email(subject: str, html_body: str, to: Optional[str] = None) -> bool:
    """Gửi HTML email qua SMTP."""
    to = to or EMAIL_ADMIN
    if not all([SMTP_USER, SMTP_PASSWORD, to]):
        logger.debug("[EMAIL] SMTP not configured — skipping")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = SMTP_USER
        msg["To"]      = to
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to, msg.as_string())
        logger.info(f"[EMAIL] Sent to {to}: {subject}")
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
    <p>Full report: {report_path}</p>
    """
    _send_email(title, html)
    logger.info(f"[NOTIFIER] Daily report sent for {stats.get('date')}")
