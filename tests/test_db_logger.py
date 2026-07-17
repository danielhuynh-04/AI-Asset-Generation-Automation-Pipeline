"""
test_db_logger.py — Unit tests for db_logger module
"""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["DB_PATH"] = ":memory:"
import db_logger


@pytest.fixture(autouse=True)
def setup_db():
    """Tạo fresh in-memory DB + rebind engine cho mỗi test."""
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    test_session = sessionmaker(bind=test_engine)
    # Monkey-patch module globals để tất cả functions dùng engine test
    db_logger.engine = test_engine
    db_logger.SessionLocal = test_session
    db_logger.Base.metadata.create_all(test_engine)
    yield
    db_logger.Base.metadata.drop_all(test_engine)


def test_create_job_returns_id():
    job_id = db_logger.create_job(
        sheet_row_id=1,
        description="Test bingo ball generation",
        model="Gemini",
        output_format="PNG",
    )
    assert isinstance(job_id, int)
    assert job_id > 0


def test_create_multiple_jobs_unique_ids():
    id1 = db_logger.create_job(1, "Job 1 description here", "Gemini", "PNG")
    id2 = db_logger.create_job(2, "Job 2 description here", "Pollinations", "JPG")
    assert id1 != id2


def test_update_job_status():
    job_id = db_logger.create_job(1, "Test asset description here", "Gemini", "PNG")
    db_logger.update_job(job_id, "RUNNING")
    db_logger.update_job(job_id, "SUCCESS", drive_url="https://drive.google.com/test", execution_time_ms=1500)

    with db_logger.SessionLocal() as session:
        job = session.get(db_logger.Job, job_id)
        assert job.status == "SUCCESS"
        assert job.drive_url == "https://drive.google.com/test"
        assert job.execution_time_ms == 1500
        assert job.finished_at is not None


def test_update_job_failed():
    job_id = db_logger.create_job(2, "Another test job description", "Pollinations", "PNG")
    db_logger.update_job(job_id, "FAILED", error_message="API timeout", retry_count=3)

    with db_logger.SessionLocal() as session:
        job = session.get(db_logger.Job, job_id)
        assert job.status == "FAILED"
        assert job.error_message == "API timeout"
        assert job.retry_count == 3


def test_get_daily_stats_empty():
    stats = db_logger.get_daily_stats()
    assert stats["total"] == 0
    assert stats["success_rate"] == 0


def test_get_daily_stats_with_jobs():
    from datetime import datetime, timezone
    id1 = db_logger.create_job(1, "Success job description here", "Gemini", "PNG")
    id2 = db_logger.create_job(2, "Failed job description here", "Gemini", "PNG")
    db_logger.update_job(id1, "SUCCESS", execution_time_ms=1000)
    db_logger.update_job(id2, "FAILED", error_message="error")

    # Dùng UTC date vì created_at lưu theo UTC (datetime.utcnow)
    utc_date = datetime.now(timezone.utc).date()
    stats = db_logger.get_daily_stats(utc_date)
    assert stats["total"] == 2
    assert stats["success"] == 1
    assert stats["failed"] == 1
    assert stats["success_rate"] == 50.0
