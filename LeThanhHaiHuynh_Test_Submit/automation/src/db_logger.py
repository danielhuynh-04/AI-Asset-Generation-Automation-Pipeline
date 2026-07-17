"""
db_logger.py — SQLite job tracking via SQLAlchemy
Manages job state transitions: PENDING → RUNNING → RETRY → SUCCESS/FAILED
"""
import os
from datetime import datetime, date
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Date, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "pipeline.db")
# Senior Level: Bật check_same_thread=False và timeout lớn để tránh lỗi "database is locked" khi ThreadPool writes
engine = create_engine(
    f"sqlite:///{DB_PATH}", 
    echo=False,
    connect_args={"check_same_thread": False, "timeout": 15}
)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "jobs"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    sheet_row_id     = Column(Integer, nullable=False)
    description      = Column(Text, nullable=False)
    example_url      = Column(String(500))
    model            = Column(String(50), nullable=False)
    output_format    = Column(String(10), nullable=False)
    status           = Column(String(20), default="PENDING")  # PENDING|RUNNING|RETRY|SUCCESS|FAILED
    retry_count      = Column(Integer, default=0)
    prompt_used      = Column(Text)
    drive_url        = Column(String(500))
    error_message    = Column(Text)
    execution_time_ms = Column(Integer)
    created_at       = Column(DateTime, default=datetime.utcnow)
    finished_at      = Column(DateTime)


class DailyReport(Base):
    __tablename__ = "reports"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    report_date   = Column(Date, nullable=False)
    total_jobs    = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failed_count  = Column(Integer, default=0)
    retry_count   = Column(Integer, default=0)
    avg_exec_ms   = Column(Float)
    success_rate  = Column(Float)
    report_path   = Column(String(500))
    sent_at       = Column(DateTime)
    created_at    = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Khởi tạo database và tạo bảng nếu chưa có."""
    Base.metadata.create_all(engine)


def create_job(sheet_row_id: int, description: str, model: str,
               output_format: str, example_url: Optional[str] = None) -> int:
    """Tạo job mới với status PENDING, trả về job_id."""
    with SessionLocal() as session:
        job = Job(
            sheet_row_id=sheet_row_id,
            description=description,
            model=model,
            output_format=output_format,
            example_url=example_url,
            status="PENDING"
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        return job.id


def update_job(job_id: int, status: str, **kwargs):
    """
    Cập nhật trạng thái và metadata của job.
    kwargs: retry_count, drive_url, error_message, execution_time_ms, prompt_used
    """
    with SessionLocal() as session:
        job = session.get(Job, job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        job.status = status
        for key, val in kwargs.items():
            if hasattr(job, key):
                setattr(job, key, val)
        if status in ("SUCCESS", "FAILED"):
            job.finished_at = datetime.utcnow()
        session.commit()


def get_daily_stats(target_date: Optional[date] = None) -> dict:
    """Trả về thống kê jobs trong một ngày (mặc định hôm nay)."""
    if target_date is None:
        target_date = date.today()
    date_str = target_date.isoformat()  # SQLite so sánh với string
    with SessionLocal() as session:
        q = session.query(Job).filter(
            func.date(Job.created_at) == date_str
        )
        total    = q.count()
        success  = q.filter(Job.status == "SUCCESS").count()
        failed   = q.filter(Job.status == "FAILED").count()
        retried  = q.filter(Job.retry_count > 0).count()
        avg_exec = session.query(func.avg(Job.execution_time_ms)).filter(
            func.date(Job.created_at) == date_str,
            Job.execution_time_ms.isnot(None)
        ).scalar()
        return {
            "date": date_str,
            "total": total,
            "success": success,
            "failed": failed,
            "retried": retried,
            "success_rate": round(success / total * 100, 1) if total > 0 else 0,
            "avg_exec_ms": round(avg_exec, 1) if avg_exec else 0,
        }


def get_jobs_for_date(target_date: Optional[date] = None) -> list[dict]:
    """Lấy danh sách toàn bộ jobs trong ngày để vẽ chart."""
    if target_date is None:
        target_date = date.today()
    date_str = target_date.isoformat()  # SQLite so sánh với string
    with SessionLocal() as session:
        jobs = session.query(Job).filter(
            func.date(Job.created_at) == date_str
        ).all()
        return [
            {
                "id": j.id,
                "description": j.description[:50],
                "model": j.model,
                "output_format": j.output_format,
                "status": j.status,
                "retry_count": j.retry_count,
                "execution_time_ms": j.execution_time_ms,
                "created_at": j.created_at,
                "finished_at": j.finished_at,
            }
            for j in jobs
        ]
