"""
main.py — Pipeline Orchestrator
Kết nối tất cả modules theo thứ tự: Read → Validate → Generate → Upload → Log → Notify
"""
import os
import sys
import time
import logging
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline.log", encoding="utf-8"),
    ]
)
logger = logging.getLogger("main")

# Import modules
sys.path.insert(0, str(Path(__file__).parent))
import db_logger
import sheets_reader
import validator
import ai_generator
import drive_uploader
import notifier
import daily_report

from retry_wrapper import retry


# ─── Retry-wrapped generator ──────────────────────────────────────────────────
@retry(max_attempts=int(os.getenv("RETRY_MAX_ATTEMPTS", "3")),
       backoff_seconds=[float(os.getenv("RETRY_BACKOFF_SECONDS", "2")), 4.0, 8.0])
def _generate_with_retry(description, model, output_format, output_path):
    return ai_generator.generate_asset(
        description=description,
        model=model,
        output_format=output_format,
        output_path=output_path,
        optimize_prompt=True,
        style_context=(
            "semi-realistic cartoon game art for Bingo mobile game, "
            "glossy shading, vibrant colors, transparent background, "
            "gold border accents, high detail, game-ready asset"
        )
    )


# ─── Process Single Row Worker ──────────────────────────────────────────────────
def _process_single_row(row: dict) -> str:
    """Xử lý đơn lẻ 1 dòng từ Google Sheet. Được gọi qua ThreadPool để chạy đa luồng."""
    row_index = row.get("_row_index", 0)
    desc_preview = str(row.get("description", ""))[:60]
    logger.info(f"\n{'─'*50}")
    logger.info(f"[ROW {row_index}] Processing: {desc_preview}")

    # 3. Validate input
    val_result = validator.validate_row(row)
    if not val_result.is_valid:
        logger.warning(f"[VALIDATE] Row {row_index} INVALID: {val_result.error}")
        job_id = db_logger.create_job(
            sheet_row_id=row_index,
            description=str(row.get("description", ""))[:500],
            model=str(row.get("model", "Unknown")),
            output_format=str(row.get("output_format", "?")),
            example_url=None,
        )
        db_logger.update_job(job_id, "FAILED", error_message=f"Validation: {val_result.error}")
        notifier.notify_failure(
            job_id=job_id,
            description=str(row.get("description", ""))[:80],
            error=val_result.error,
            retry_count=0,
            output_format=str(row.get("output_format", "?")),
        )
        try:
            sheets_reader.update_row_status(
                os.getenv("GOOGLE_SHEET_ID"), row_index, "FAILED"
            )
        except Exception as e:
            logger.warning(f"[SHEETS] Could not write-back status: {e}")
        return "failed"

    norm = val_result.normalized

    if norm.get("url_warning"):
        logger.warning(f"[VALIDATE] {norm['url_warning']}")

    # 4. Create job record
    job_id = db_logger.create_job(
        sheet_row_id=row_index,
        description=norm["description"],
        model=norm["model"],
        output_format=norm["output_format"],
        example_url=norm["example_url"],
    )
    db_logger.update_job(job_id, "RUNNING")
    logger.info(f"[JOB {job_id}] Created — Model: {norm['model']}, Format: {norm['output_format']}")

    # 5. Generate asset
    output_dir  = os.getenv("OUTPUT_DIR", "outputs")
    ext         = norm["output_format"].lower()
    local_path  = f"{output_dir}/{date.today().isoformat()}/{norm['output_format']}/job_{job_id:04d}.{ext}"
    retry_count = 0
    try:
        result = _generate_with_retry(
            norm["description"], norm["model"], norm["output_format"], local_path
        )
        logger.info(f"[JOB {job_id}] Generated in {result['duration_ms']}ms via {result['model_used']}")

        # 6. Upload to Google Drive (Try-except để không làm hỏng pipeline nếu API chặn)
        try:
            drive_url = drive_uploader.upload_asset(
                local_path=result["output_path"],
                job_id=job_id,
                output_format=norm["output_format"],
            )
        except Exception as e_drive:
            logger.warning(f"[DRIVE] Upload failed (Quota/Permission): {e_drive}. Using local path.")
            drive_url = f"file://{os.path.abspath(result['output_path'])}"

        # 7. Update DB — SUCCESS
        db_logger.update_job(
            job_id, "SUCCESS",
            drive_url=drive_url,
            prompt_used=result["prompt_used"],
            execution_time_ms=result["duration_ms"],
            retry_count=retry_count,
        )

        notifier.notify_success(
            job_id=job_id,
            description=norm["description"],
            drive_url=drive_url,
            model_used=result["model_used"],
            duration_ms=result["duration_ms"],
        )

        try:
            sheets_reader.update_row_status(
                os.getenv("GOOGLE_SHEET_ID"), row_index, "DONE"
            )
        except Exception as e:
            logger.warning(f"[SHEETS] Could not write-back status: {e}")

        return "success"

    except Exception as e:
        retry_count = getattr(e, "retry_count", 3)
        logger.error(f"[JOB {job_id}] FAILED after {retry_count} retries: {e}")
        db_logger.update_job(job_id, "FAILED", error_message=str(e), retry_count=retry_count)
        notifier.notify_failure(
            job_id=job_id,
            description=norm["description"],
            error=str(e),
            retry_count=retry_count,
            output_format=norm["output_format"],
        )
        try:
            sheets_reader.update_row_status(
                os.getenv("GOOGLE_SHEET_ID"), row_index, "FAILED"
            )
        except Exception as e_sheet:
            logger.warning(f"[SHEETS] Could not write-back status: {e_sheet}")
        return "failed"


# ─── Main pipeline ────────────────────────────────────────────────────────────
def run_pipeline():
    """
    Luồng xử lý chính:
    1. Init DB
    2. Read Google Sheet
    3. For each row: Validate → Create Job → Generate → Upload → Update
    4. Log kết quả từng bước
    """
    logger.info("=" * 60)
    logger.info("[START] AI Asset Generation Pipeline")
    logger.info(f"[DATE] {date.today().isoformat()}")
    logger.info("=" * 60)

    # 1. Init database
    db_logger.init_db()
    logger.info("[INIT] Database initialized")

    # 2. Read Google Sheet
    try:
        rows = sheets_reader.read_pending_rows()
    except FileNotFoundError as e:
        logger.error(f"[SHEETS] {e}")
        logger.error("Please complete Google Cloud setup (see README.md Step 0)")
        sys.exit(1)
    except Exception as e:
        logger.error(f"[SHEETS] Failed to read: {e}")
        sys.exit(1)

    if not rows:
        logger.info("[PIPELINE] No pending rows — done.")
        return

    logger.info(f"[PIPELINE] Processing {len(rows)} rows concurrently (max_workers=2)...")
    summary = {"total": len(rows), "success": 0, "failed": 0, "skipped": 0}

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Chạy đa luồng song song (giảm xuống 2 để tránh 429 Too Many Requests từ Pollinations)
        results = executor.map(_process_single_row, rows)
    
    for res in results:
        if res in summary:
            summary[res] += 1

    # Final summary log
    logger.info("\n" + "=" * 60)
    logger.info("[DONE] PIPELINE COMPLETE")
    logger.info(f"   Total:   {summary['total']}")
    logger.info(f"   Success: {summary['success']}")
    logger.info(f"   Failed:  {summary['failed']}")
    logger.info(f"   Skipped: {summary['skipped']}")
    logger.info("=" * 60)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI Asset Generation Pipeline")
    parser.add_argument("--report-only", action="store_true", help="Only generate daily report")
    parser.add_argument("--with-scheduler", action="store_true", help="Start daily report scheduler")
    args = parser.parse_args()

    if args.report_only:
        path = daily_report.generate_report()
        print(f"Report: {path}")
    else:
        if args.with_scheduler:
            scheduler = daily_report.start_scheduler()
        run_pipeline()
