"""
daily_report.py — Analytics Report Module
Query SQLite DB → tính thống kê → vẽ Plotly charts → export HTML/PNG → email admin
APScheduler trigger lúc 23:00 mỗi ngày.
"""
import os
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import plotly.graph_objects as go
import plotly.subplots as ps
import pandas as pd
from dotenv import load_dotenv

import db_logger
import notifier

load_dotenv()
logger = logging.getLogger(__name__)

REPORT_DIR = os.getenv("REPORT_DIR", "report_sample")
REPORT_HOUR   = int(os.getenv("REPORT_SCHEDULE_HOUR", "23"))
REPORT_MINUTE = int(os.getenv("REPORT_SCHEDULE_MINUTE", "0"))


def generate_report(target_date: Optional[date] = None, run_now: bool = False) -> str:
    """
    Tạo daily report:
    1. Query DB
    2. Vẽ 4 charts (Pie success rate, Bar jobs/hour, Scatter exec time, status distribution)
    3. Export HTML
    4. Email admin
    5. Lưu vào bảng reports

    Returns:
        Path tới file HTML report
    """
    if target_date is None:
        target_date = date.today()

    stats = db_logger.get_daily_stats(target_date)
    jobs  = db_logger.get_jobs_for_date(target_date)

    if stats["total"] == 0:
        logger.info(f"[REPORT] No jobs for {target_date} — skipping report")
        return ""

    df = pd.DataFrame(jobs)

    # ── Chart 1: Pie — Success vs Failed ──────────────────────────────────────
    pie_fig = go.Figure(go.Pie(
        labels=["Success ✅", "Failed ❌", "Pending ⏳"],
        values=[stats["success"], stats["failed"],
                stats["total"] - stats["success"] - stats["failed"]],
        marker_colors=["#2ecc71", "#e74c3c", "#f39c12"],
        hole=0.4,
        textinfo="label+percent",
    ))
    pie_fig.update_layout(title="Job Success Rate")

    # ── Chart 2: Bar — Jobs by Hour ───────────────────────────────────────────
    if "created_at" in df.columns and len(df) > 0:
        df["hour"] = pd.to_datetime(df["created_at"]).dt.hour
        hour_counts = df.groupby("hour")["id"].count().reset_index()
        bar_fig = go.Figure(go.Bar(
            x=hour_counts["hour"],
            y=hour_counts["id"],
            marker_color="#3498db",
            text=hour_counts["id"],
            textposition="outside",
        ))
        bar_fig.update_layout(
            title="Jobs Processed per Hour",
            xaxis_title="Hour of Day",
            yaxis_title="Job Count",
        )
    else:
        bar_fig = go.Figure()
        bar_fig.update_layout(title="Jobs per Hour — No data")

    # ── Chart 3: Scatter — Execution Time per Job ─────────────────────────────
    if "execution_time_ms" in df.columns and df["execution_time_ms"].notna().any():
        color_map = {"SUCCESS": "#2ecc71", "FAILED": "#e74c3c", "RETRY": "#f39c12", "PENDING": "#95a5a6"}
        scatter_fig = go.Figure()
        for status, color in color_map.items():
            subset = df[df["status"] == status]
            if len(subset) > 0:
                scatter_fig.add_trace(go.Scatter(
                    x=list(range(len(subset))), y=subset["execution_time_ms"],
                    mode="markers", name=status,
                    marker=dict(color=color, size=10),
                    text=subset["description"],
                ))
        scatter_fig.update_layout(
            title="Execution Time per Job (ms)",
            xaxis_title="Job Index", yaxis_title="Execution Time (ms)"
        )
    else:
        scatter_fig = go.Figure()
        scatter_fig.update_layout(title="Execution Time — No data")

    # ── Chart 4: Bar — Status Distribution by Model ───────────────────────────
    if "model" in df.columns and len(df) > 0:
        model_status = df.groupby(["model", "status"])["id"].count().reset_index()
        model_status.columns = ["model", "status", "count"]
        bar2_fig = go.Figure()
        statuses = model_status["status"].unique()
        colors2  = {"SUCCESS": "#2ecc71", "FAILED": "#e74c3c", "RETRY": "#f39c12", "PENDING": "#95a5a6", "RUNNING": "#3498db"}
        for s in statuses:
            subset2 = model_status[model_status["status"] == s]
            bar2_fig.add_trace(go.Bar(
                x=subset2["model"], y=subset2["count"],
                name=s, marker_color=colors2.get(s, "#bdc3c7")
            ))
        bar2_fig.update_layout(
            title="Job Status by AI Model",
            barmode="group",
            xaxis_title="Model", yaxis_title="Count"
        )
    else:
        bar2_fig = go.Figure()
        bar2_fig.update_layout(title="Status by Model — No data")

    # ── Assemble HTML report ───────────────────────────────────────────────────
    report_dir = Path(REPORT_DIR)
    report_dir.mkdir(parents=True, exist_ok=True)
    out_path = report_dir / f"daily_report_{target_date.isoformat()}.html"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Daily Report — {target_date}</title>
    <style>
      body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 20px; }}
      h1   {{ color: #00d4ff; text-align: center; }}
      .stats {{ display: flex; gap: 20px; justify-content: center; margin: 20px 0; flex-wrap: wrap; }}
      .card  {{ background: #16213e; border-radius: 12px; padding: 24px 36px; text-align: center; }}
      .card .num {{ font-size: 2.5rem; font-weight: bold; color: #00d4ff; }}
      .card .label {{ color: #aaa; margin-top: 4px; }}
      .green  {{ color: #2ecc71 !important; }}
      .red    {{ color: #e74c3c !important; }}
      .charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 24px; }}
      .chart-box {{ background: #16213e; border-radius: 12px; padding: 16px; }}
    </style>
</head>
<body>
    <h1>📊 Daily Pipeline Report — {target_date}</h1>
    <div class="stats">
      <div class="card"><div class="num">{stats['total']}</div><div class="label">Total Jobs</div></div>
      <div class="card"><div class="num green">{stats['success']}</div><div class="label">Success</div></div>
      <div class="card"><div class="num red">{stats['failed']}</div><div class="label">Failed</div></div>
      <div class="card"><div class="num">{stats['success_rate']}%</div><div class="label">Success Rate</div></div>
      <div class="card"><div class="num">{stats['avg_exec_ms']}ms</div><div class="label">Avg Time</div></div>
    </div>
    <div class="charts">
      <div class="chart-box">{pie_fig.to_html(full_html=False, include_plotlyjs='cdn')}</div>
      <div class="chart-box">{bar_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
      <div class="chart-box">{scatter_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
      <div class="chart-box">{bar2_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
    </div>
</body>
</html>""")

    logger.info(f"[REPORT] Generated: {out_path}")

    # Email admin
    notifier.notify_daily_report(str(out_path), stats)

    # Lưu vào DB
    with db_logger.SessionLocal() as session:
        report = db_logger.DailyReport(
            report_date=target_date,
            total_jobs=stats["total"],
            success_count=stats["success"],
            failed_count=stats["failed"],
            retry_count=stats["retried"],
            avg_exec_ms=stats["avg_exec_ms"],
            success_rate=stats["success_rate"],
            report_path=str(out_path),
            sent_at=datetime.utcnow(),
        )
        session.add(report)
        session.commit()

    return str(out_path)


def start_scheduler():
    """Khởi động APScheduler để tự chạy report lúc 23:00 mỗi ngày."""
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=generate_report,
        trigger="cron",
        hour=REPORT_HOUR,
        minute=REPORT_MINUTE,
        id="daily_report",
        name="Daily Pipeline Report",
    )
    scheduler.start()
    logger.info(f"[SCHEDULER] Daily report scheduled at {REPORT_HOUR:02d}:{REPORT_MINUTE:02d}")
    return scheduler


if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-now", action="store_true", help="Generate report immediately")
    parser.add_argument("--date", type=str, help="Date YYYY-MM-DD (default: today)")
    args = parser.parse_args()

    target = date.fromisoformat(args.date) if args.date else None
    path  = generate_report(target_date=target, run_now=args.run_now)
    if path:
        print(f"Report saved: {path}")
