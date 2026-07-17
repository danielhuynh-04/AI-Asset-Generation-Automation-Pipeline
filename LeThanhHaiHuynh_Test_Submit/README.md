# AI Asset Generation Automation Pipeline
### Athena Studio — Prompt Engineer / Automation Engineer Intern Test
**Ứng viên:** Lê Thanh Hải Huỳnh (Daniel Huynh) | [GitHub](https://github.com/danielhuynh-04) | [Kaggle](https://kaggle.com/lthanhhihunh)

> **Tiếp cận:** Toàn bộ automation workflow được thiết kế như một **data pipeline có kiểm soát chất lượng** — validate input tại nguồn, kiểm soát lỗi tại từng bước, log đầy đủ state, và đánh giá kết quả bằng số liệu cụ thể. Nguyên tắc tôi đã áp dụng khi xây dựng hệ thống dự báo dịch bệnh Dengue với R² = 0.966.

## 🔥 Production-Ready Architecture (System Mindset)

Bài test này không dừng lại ở mức kịch bản chạy tự động (Scripting) mà được thiết kế theo tư duy của một **Data Pipeline tiêu chuẩn thực tế (Production-ready)**:

1. **Multi-threaded I/O (Xử lý Đa Luồng):** Chuyển vòng lặp xử lý tuần tự sang `concurrent.futures.ThreadPoolExecutor(max_workers=5)`, giúp gọi API AI và Google Drive **song song**, xử lý hàng trăm tấm ảnh trong không gian thời gian bị block thấp nhất.
2. **Resilient LLM Fallback (Chống đứt đoạn System & Xử lý 429):** Khai thác triệt để chiến thuật Multi-Model. Mặc định gọi *Gemini Pro*. Nếu API hất văng vì **HTTP 429 Too Many Requests / Quota Exceeded**, hệ thống dựa vào Exponential Backoff lỳ đòn quay xe Fallback sang **ChatGPT (Pollinations)**. Lỗi không bao giờ gây Crash (Zero-Crash), bảo toàn thông lượng đa luồng. Hơn thế, các công việc thất bại kiệt sức 3 Retries sẽ được **đồng bộ ngược trạng thái FAILED về thẳng Google Sheets** phục vụ đối soát 2 chiều hoàn hảo.
3. **Thread-Safe State Machine (Ghi Log an toàn):** Với môi trường đa luồng, SQLite được tinh chỉnh qua SQLAlchemy `connect_args={"check_same_thread": False, "timeout": 15}` giúp Transactions an toàn tuyệt đối, triệt tiêu lỗi deadlocks (database is locked).
4. **Enterprise Zero-Trust Security (Bảo mật tuyệt đối):** Loại bỏ hoàn toàn phương thức gửi Email rủi ro bằng SMTP/App Password. Tích hợp trực tiếp **Gmail API qua chuẩn OAuth 2.0 Web Consent**, thiết lập file Tokens độc lập theo nguyên tắc Least Privilege (Drive và Gmail không xâm phạm quyền của nhau).
5. **Decoupled Architecture & Idempotency:** Hệ thống có khả năng ngắt quãng và chạy lại mà không bị sinh trùng lặp ảnh (chỉ chạy dòng chưa DONE). Module báo cáo (Analytics Report) chạy Process tách biệt bằng APScheduler để không làm nặng luồng Main.

---

## 📅 5-Day Project Timeline (Execution Plan)

> Thể hiện tư duy Quản lý dự án (Project Management) và phân bổ nguồn lực khoa học, đảm bảo giao hàng (delivery) đúng deadline.

```mermaid
gantt
    title Athena Asset Automation Pipeline 5 Days Plan
    dateFormat  YYYY-MM-DD
    axisFormat  %Y-%m-%d
    
    section Day 1 Setup
    Requirement Analysis     :done,    des1, 2026-07-13, 1d
    System Design & ERD      :done,    des2, 2026-07-13, 1d
    Environment Setup        :done,    des3, 2026-07-13, 1d
    
    section Day 2 Core
    Modules coding           :done,    dev1, 2026-07-14, 1d
    Database & Retry Logic   :done,    dev2, 2026-07-14, 1d
    Integration & Tests      :done,    dev3, 2026-07-14, 1d
    
    section Day 3 Prompting
    Asset Style Analysis     :done,    pe1, 2026-07-15, 1d
    Iterative Prompting V1X  :done,    pe2, 2026-07-15, 1d
    Prompt Eng Report        :done,    pe3, 2026-07-15, 1d
    
    section Day 4 Reporting
    Daily Report Plotly      :done,    rep1, 2026-07-16, 1d
    Slack Notifications      :done,    rep2, 2026-07-16, 1d
    Documentation README     :done,    rep3, 2026-07-16, 1d
    
    section Day 5 Submission
    Final Packaging Cleanup  :done,    sub1, 2026-07-17, 1d
    Video Presentation       :active,  sub2, 2026-07-17, 1d
    Submit to HR             :active,  sub3, 2026-07-17, 1d
```

---

## 🏗️ System Architecture & Workflow

Đây là kiến trúc luồng dữ liệu chính của AI Asset Pipeline. Hệ thống được thiết kế với tư duy Module hóa cao (Decoupled architecture) và khả năng phục hồi lỗi (Fault-tolerant).

```mermaid
graph TD
    A[Google Sheets<br>Data Input] -->|Read Pending Rows| B(src/sheets_reader.py);
    B -->|Raw Rows| C{src/validator.py};
    
    C -- Invalid --> D[src/db_logger.py<br>Mark FAILED];
    C -- Valid --> E(src/main.py<br>ThreadPoolExecutor);
    
    E -->|Dispatch| F[src/ai_generator.py];
    
    subgraph AI Generation Engine
       F -->|Try 1: Gemini Pro| G[Google Gemini API]
       G -.->|Quota Exceeded| H[Pollinations AI Fallback]
       G -.->|Timeout| I[retry_wrapper.py<br>Exponential Backoff]
    end
    
    G --> J(Asset Generated);
    H --> J;
    
    J -->|Upload| K[src/drive_uploader.py];
    K -->|Store| L[(Google Drive)];
    
    J -->|Log Status| D;
    D -->|Write| M[(SQLite Database)];
    
    J -->|URL & Status| N[src/notifier.py];
    N -->|Slack Webhook| O[Slack Alerts];
    N -->|OAuth 2.0| P[Gmail Alerts];
    
    Q((APScheduler)) -.->|Trigger 23:00| R[src/daily_report.py];
    M -.->|Query Stats| R;
    R -->|Plotly Charts| S[HTML Dashboard];
    S --> P;
```

## 🔄 Business Process Model (BPMN)

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant System as Orchestrator (main.py)
    participant AI as AI Services (Gemini/Pollinations)
    participant Storage as Storage (Drive/SQLite)
    participant Notif as Notifications (Slack/Email)

    User->>Storage: 1. Input Prompt to Google Sheets
    System->>Storage: 2. Fetch PENDING Rows
    Storage-->>System: Return Rows Data
    
    Note over System, AI: Execution Loop (Concurrent)
    System->>System: 3. Validate Data Format
    
    alt is Valid
        System->>AI: 4. Request Asset Generation
        AI-->>System: Return Image/Audio Bytes (Success)
        System->>Storage: 5. Upload File to Google Drive
        Storage-->>System: Return Shareable URL
        System->>Storage: 6. Update SQLite Status (SUCCESS)
        System->>Notif: 7. Trigger notify_success()
        Notif-->>User: Slack/Email Success Alert
    else is Invalid or AI Failed
        AI-->>System: Timeout/Error after 3 Retries
        System->>Storage: 8. Update SQLite Status (FAILED)
        System->>Notif: 9. Trigger notify_failure()
        Notif-->>User: Slack/Email Error Alert
    end
    
    Note over System, Notif: Asynchronous Daily Reporting
    System-->>System: 10. Trigger at 23:00 (APScheduler)
    System->>Storage: 11. Query Daily Stats
    System->>System: 12. Generate Plotly HTML Dashboard
    System->>Notif: 13. Send Dashboard Summary
    Notif-->>User: Final Daily Report Email
```

---

## Quick Start

### 1. Clone & Environment
```bash
git clone https://github.com/danielhuynh-04/athena-prompt-automation-test
cd athena-prompt-automation-test
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 2. Google Cloud Setup (REQUIRED — làm một lần)

> **Bước 0: Xem hướng dẫn chi tiết trong [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md)**

**Tóm tắt nhanh:**
1. [Tạo Google Cloud Project](https://console.cloud.google.com) → bật Sheets API, Drive API, Generative Language API
2. Tạo Service Account → download JSON → đặt tên `credentials.json` ở root project
3. [Lấy Gemini API key](https://aistudio.google.com/app/apikey)
4. Tạo Google Sheet, share với email service account, copy Sheet ID
5. Lấy **Slack Webhook URL**: [Tạo Slack Webhook](https://api.slack.com/messaging/webhooks) (Tạo App, bật Incoming Webhooks, copy link).
6. [Tạo OAuth Client ID](https://console.cloud.google.com/apis/credentials/oauthclient) tải file `client_secret.json` về (phục vụ Upload Google Drive).

### 3. Cấu hình `.env`
```bash
cp .env.example .env
# Mở .env và điền các giá trị thực:
# GEMINI_API_KEY, GOOGLE_SHEET_ID, GOOGLE_DRIVE_FOLDER_ID, SLACK_WEBHOOK_URL, SMTP credentials
```

### 4. Chạy Pipeline
```bash
cd src
python main.py
```

### 5. Các lệnh khác
```bash
# Chỉ generate daily report
python src/main.py --report-only

# Pipeline + bật scheduler (tự report lúc 23:00)
python src/main.py --with-scheduler

# Generate report cho ngày cụ thể
python src/daily_report.py --run-now --date 2026-07-14

# Chạy unit tests
python -m pytest tests/ -v
```

---

## Google Sheet Format

| Cột | Loại | Mô tả |
|---|---|---|
| `id` | số | Unique row ID |
| `description` | text | Mô tả asset (bắt buộc, tối thiểu 10 ký tự) |
| `example_url` | URL | Ảnh mẫu tham khảo (tùy chọn) |
| `output_format` | PNG/JPG/GIF/MP3 | Định dạng output |
| `model` | Gemini/Pollinations | AI model dùng để generate |
| `status` | auto | Pipeline ghi: DONE / FAILED |

---

## 🧪 Comprehensive Test Cases (100% Covered)

Đề bài yêu cầu 4 test cases bắt buộc. Bạn có thể tự mô phỏng trong Google Sheets như sau:

| Test Case | Cách giả lập trong Google Sheet | Expected Behavior |
|---|---|---|
| **✅ 1. Job thành công** | Điền chuỗi hợp lệ vào description | AI sinh ảnh/âm thanh, lưu Drive, báo Slack SUCCESS, `status=DONE`. |
| **❌ 2. Sai URL example** | Điền `http://xyz` không hợp lệ | Pipeline ghi log Thẻ `[VALIDATE] WARNING`, vẫn ráng chạy nhưng bỏ qua URL lỗi. |
| **❌ 3. API Timeout** | Điền có chứa chữ **`MOCK_TIMEOUT`** vào description | Pipeline tự động bắt từ khoá, raise `TimeoutError`, Retry 3 lần, fail & báo Slack. |
| **❌ 4. Sai Format** | Điền `WEBP` hoặc `MP4` vào format | Validator chặn cứng từ vòng gửi xe, đánh `FAILED`, báo qua Slack. |

---

## AI Models

| Model | Chi tiết | Giới hạn |
|---|---|---|
| **Gemini Imagen 3** | `imagen-3.0-generate-002` — chất lượng cao | 10 ảnh/ngày (free tier) |
| **Pollinations.ai** | Miễn phí, không cần key, dùng Flux model | Không giới hạn |
| **gTTS** | Google Text-to-Speech cho MP3 | Miễn phí |
| **Gemini Pro Flash** | Tối ưu hóa prompt trước khi generate | 1500 req/ngày |

> **Lưu ý kỹ thuật:** Claude (Anthropic) không sinh ảnh trực tiếp. Kiến trúc này dùng Gemini cho cả text optimization và image generation — tiết kiệm chi phí và đơn giản hóa dependencies.

---

## Job State Machine

```
PENDING → RUNNING → SUCCESS
                 ↘
           RETRY (1-3) → SUCCESS
                       ↘ FAILED
PENDING → FAILED (validation error — không qua AI)
```

---

## Output Structure

```
outputs/
└── 2026-07-14/
    ├── PNG/
    │   ├── job_0001_1720900000.png
    │   └── job_0003_1720900050.png
    ├── JPG/
    │   └── job_0002_1720900020.jpg
    └── MP3/
        └── job_0004_1720900080.mp3
```

Google Drive mirror: `Outputs/{date}/{format}/{filename}`

---

## Known Limitations & Future Work

| Limitation | Future Improvement |
|---|---|
| Gemini Imagen: 10 ảnh/ngày free tier | Queue worker + paid tier hoặc mix với Pollinations |
| APScheduler in-process (dừng khi script tắt) | Migrate sang Celery + Redis cho production |
| SQLite: single-file, no concurrent writes | Postgres cho multi-user / high volume |
| No deduplication by prompt hash | Cache layer: SHA256(prompt) → skip re-generation |
| Pollinations.ai public API (no SLA) | Self-hosted Stable Diffusion via HuggingFace |

---

## Project Structure

```
├── src/
│   ├── main.py              # Pipeline orchestrator
│   ├── sheets_reader.py     # Google Sheets ingestion
│   ├── validator.py         # Input validation
│   ├── ai_generator.py      # Gemini Imagen + Pollinations + gTTS
│   ├── retry_wrapper.py     # Exponential backoff decorator
│   ├── drive_uploader.py    # Google Drive upload
│   ├── db_logger.py         # SQLAlchemy job tracking
│   ├── notifier.py          # Slack + Email alerts
│   └── daily_report.py      # Plotly analytics + APScheduler
├── docs/                    # Requirement analysis, system design
├── database/                # schema.sql + ERD
├── prompt_engineering/      # Report + iteration images
│   ├── PROMPT_ENGINEERING_REPORT_EN.md
│   ├── prompt_engineering_report.md
│   └── iterations/          # V1/V2/V3 per asset type
├── tests/                   # pytest unit tests
├── report_sample/           # Sample daily report output
├── .env.example             # Config template
├── SCRIPT_CHI_TIET_TIENG_VIET.md  # Kịch bản đọc Video SIÊU CHI TIẾT (VN)
├── SCRIPT_DETAILED_ENGLISH.md     # Ultra-detailed Video Script (EN)
├── requirements.txt
└── README.md
```
