-- ============================================================
-- AI Asset Generation Automation Pipeline
-- Database Schema (SQLite via SQLAlchemy)
-- ============================================================

-- Bảng chính: theo dõi từng job từ Google Sheets
CREATE TABLE IF NOT EXISTS jobs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sheet_row_id    INTEGER NOT NULL,           -- Row index trong Google Sheet
    description     TEXT NOT NULL,              -- Mô tả asset cần generate
    example_url     TEXT,                       -- URL ảnh mẫu tham khảo (optional)
    model           TEXT NOT NULL,              -- 'Gemini' | 'Pollinations'
    output_format   TEXT NOT NULL,              -- 'PNG' | 'JPG' | 'GIF' | 'MP3'
    status          TEXT DEFAULT 'PENDING',     -- PENDING | RUNNING | RETRY | SUCCESS | FAILED
    retry_count     INTEGER DEFAULT 0,
    prompt_used     TEXT,                       -- Prompt thực tế gửi đến AI
    drive_url       TEXT,                       -- URL file trên Google Drive sau upload
    error_message   TEXT,                       -- Nội dung lỗi nếu failed
    execution_time_ms INTEGER,                  -- Tổng thời gian xử lý (ms)
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at     TIMESTAMP
);

-- Bảng daily reports: tổng hợp mỗi ngày
CREATE TABLE IF NOT EXISTS reports (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date     DATE NOT NULL,
    total_jobs      INTEGER NOT NULL DEFAULT 0,
    success_count   INTEGER NOT NULL DEFAULT 0,
    failed_count    INTEGER NOT NULL DEFAULT 0,
    retry_count     INTEGER NOT NULL DEFAULT 0,
    avg_exec_ms     FLOAT,
    success_rate    FLOAT,                      -- success_count / total_jobs * 100
    report_path     TEXT,                       -- Path tới file HTML report xuất ra
    sent_at         TIMESTAMP,                  -- Thời điểm đã email report
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index để query nhanh theo status và ngày
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_created ON jobs(DATE(created_at));
CREATE INDEX IF NOT EXISTS idx_reports_date ON reports(report_date);
