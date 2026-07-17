# Requirement Analysis
## Project: AI Asset Generation Automation Pipeline
## Vị trí: Prompt Engineer / Automation Engineer Intern — Athena Studio
### Ngày: 2026-07-14

---

## 1. Objective

Build an end-to-end AI automation workflow capable of:
- **FR-01** Reading asset generation requests from Google Sheets
- **FR-02** Validating each input row (null check, format check, model routing)
- **FR-03** Generating visual game assets via AI (Gemini Imagen / Pollinations.ai)
- **FR-04** Uploading generated assets to Google Drive with structured folder naming
- **FR-05** Logging all job states to a relational database (SQLite)
- **FR-06** Sending real-time Slack notifications (success + failure)
- **FR-07** Sending Email notifications via SMTP
- **FR-08** Generating daily summary reports with analytics charts (Plotly)

---

## 2. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Read rows from Google Sheets via service account API | HIGH |
| FR-02 | Validate each row: non-null description, valid output_format (PNG/JPG/GIF/MP3), valid model | HIGH |
| FR-03 | Generate image asset using Gemini Imagen 3 or Pollinations.ai fallback | HIGH |
| FR-04 | Generate audio asset (MP3) using gTTS | MEDIUM |
| FR-05 | Upload generated asset to Google Drive under `Outputs/{date}/{format}/` | HIGH |
| FR-06 | Update job status in SQLite DB at each pipeline stage | HIGH |
| FR-07 | Send Slack notification on job SUCCESS and FAILURE | MEDIUM |
| FR-08 | Send Email notification on job SUCCESS and FAILURE | MEDIUM |
| FR-09 | Generate daily analytics report (Pie/Bar/Timeline charts) via Plotly | MEDIUM |
| FR-10 | Schedule daily report via APScheduler at 23:00 | LOW |
| FR-11 | Write prompt optimization prompt via Gemini Pro text before image generation | MEDIUM |

---

## 3. Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Reliability** | Retry failed API calls up to 3 times with exponential backoff (2s, 4s, 8s) |
| **Fault Tolerance** | Invalid rows must be skipped and logged — pipeline must NOT crash |
| **Scalability** | Module-based design allows adding new AI providers or output formats without core change |
| **Observability** | Every job must have full state trail: PENDING → RUNNING → RETRY → SUCCESS/FAILED |
| **Security** | No API keys in source code — dotenv pattern only |
| **Maintainability** | Each module independently testable; clear function contracts |
| **Idempotency** | Rows already marked `status=DONE` in Sheet must be skipped on re-run |

---

## 4. System Constraints

| Constraint | Detail |
|---|---|
| AI Image Model | Gemini Imagen 3 (free tier: 10 images/day) → Pollinations.ai fallback (unlimited, free) |
| AI Text Model | Gemini Pro Flash (gemini-2.0-flash, free tier) |
| Audio Model | gTTS (Google Text-to-Speech, free) |
| Database | SQLite (local) — no cloud DB required |
| Notification | Slack webhook (free) + Gmail SMTP with App Password |
| Scheduling | APScheduler (in-process) — no Celery/Redis required |
| Runtime | Python 3.11+, Windows OS |

---

## 5. Input/Output Specification

### Input: Google Sheet row
| Column | Type | Constraint |
|---|---|---|
| id | int | unique row identifier |
| description | str | NOT NULL, min 10 chars |
| example_url | str | optional, valid URL format |
| output_format | str | one of: PNG, JPG, GIF, MP3 |
| model | str | one of: Gemini, Pollinations |
| status | str | pipeline writes back: DONE, FAILED |

### Output: Google Drive
- Folder path: `Outputs/{YYYY-MM-DD}/{output_format}/{job_id}_{timestamp}.{ext}`
- Shareable public URL logged to database

---

## 6. Out of Scope (for this test)
- Queue-based worker system (Celery/Redis) — noted as future improvement
- Web UI dashboard
- Multi-user authentication
- Cost tracking / rate limit management
