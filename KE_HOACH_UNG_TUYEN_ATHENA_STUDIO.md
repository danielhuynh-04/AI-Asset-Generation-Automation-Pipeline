# KẾ HOẠCH ỨNG TUYỂN & THỰC HIỆN BÀI TEST
## Vị trí: Prompt Engineer / Automation Engineer Intern — Athena Studio
### Ứng viên: Lê Thanh Hải Huỳnh (Daniel Huynh)

---

## 1. CHIẾN LƯỢC TỔNG THỂ: BIẾN NỀN TẢNG CỦA BẠN THÀNH LỢI THẾ

Bạn không đến từ nền web-dev/automation truyền thống — bạn đến từ **Data Science / Graph ML / ERP**. Đừng cố "diễn" như một automation engineer thuần túy. Thay vào đó, định vị bài test này như một **data pipeline engineering problem**, đúng thế mạnh bạn đã chứng minh qua đồ án Dengue Forecasting và ERP Odoo.

| Yêu cầu đề bài | Bạn đã từng làm gì tương đương | Cách khai thác trong bài nộp |
|---|---|---|
| Thiết kế workflow nhiều bước, nhiều nguồn dữ liệu | Pipeline GNN: 14 features → weekly graph snapshots → 5 kiến trúc → benchmark | Trình bày Automation workflow như một **data pipeline có validation, logging, checkpoint** — không chỉ là "script chạy for loop" |
| Database logging, schema thiết kế | SSMS, pgAdmin, PowerDesigner, thiết kế bảng quan hệ | Thiết kế schema `jobs` chuẩn hoá, có ERD — điểm cộng lớn vì đa số ứng viên chỉ tạo 1 bảng phẳng |
| Xử lý lỗi, validation, leakage-control | Temporal train/val/test split, leakage scan, permutation test | Áp tư duy "kiểm soát rủi ro dữ liệu" sang retry/error handling — bạn hiểu rõ *tại sao* phải kiểm soát, không chỉ *làm sao* |
| Report + chart cuối ngày | Dashboard Plotly/Mapbox cho outbreak risk | Daily Report dùng **Plotly** (không cần học Matplotlib từ đầu) — tái sử dụng kỹ năng sẵn có |
| Quản lý tiến độ 5 ngày, tài liệu hoá | CPO certified — Gantt chart, WBS, milestone tracking | Đính kèm 1 Gantt chart nhỏ trong README — thể hiện tư duy PM, hiếm ứng viên intern có |
| Giải thích kỹ thuật rõ ràng | Research proposal, thesis defense, Kaggle publish | Video trình bày như một "mini defense" — mạch lạc, có số liệu, có giới hạn/hướng cải tiến |

**Thông điệp xuyên suốt khi trình bày (CV note, video, README):** *"Tôi tiếp cận automation workflow này như một data pipeline có kiểm soát chất lượng — áp dụng nguyên tắc tôi đã dùng khi xây dựng hệ thống dự báo dịch bệnh: validate input, kiểm soát lỗi tại từng bước, log đầy đủ, và đánh giá bằng số liệu cụ thể."* Đây là câu chuyện khác biệt so với 90% ứng viên chỉ nộp code chạy được.

---

## 2. KIẾN TRÚC HỆ THỐNG ĐỀ XUẤT

```
Google Sheets (input: description, asset_url, output_format, model)
        │
        ▼
[1] Extract & Validate  ──── sai định dạng/thiếu field → log lỗi, skip, KHÔNG crash
        │
        ▼
[2] Router theo output_format (PNG/JPG/GIF/MP3) và model (OpenAI/Claude)
        │
        ▼
[3] AI Generation Service ──── retry (3 lần, exponential backoff) → vẫn fail → log + alert
        │
        ├──────────────┬───────────────┐
        ▼              ▼               ▼
   Google Drive     SQLite/Postgres   Slack + Email
   (lưu theo        (bảng jobs:       (thông báo
   folder/date)      status, error,    success/fail
                      retry_count,     theo từng job)
                      drive_url)
        │
        ▼
[4] Daily Report Scheduler (cron/APScheduler, chạy độc lập cuối ngày)
        │
        ▼
   Query DB → tính success/fail rate → vẽ Pie/Bar chart (Plotly) → email admin
```

**Vì sao tách Daily Report thành luồng độc lập:** nếu chạy chung với luồng xử lý ảnh, một lỗi ở report sẽ ảnh hưởng job đang chạy. Tách riêng = đúng nguyên tắc bạn đã áp dụng khi tách train/val/test theo thời gian để tránh nhiễu chéo.

---

## 3. LỊCH TRÌNH 5 NGÀY — CHI TIẾT TỪNG BƯỚC

### NGÀY 1 — Thiết kế & Dựng nền

**Buổi sáng: Setup**
- Tạo repo Git: `athena-prompt-automation-test`
- Tạo virtual env, `requirements.txt` (google-api-python-client, openai, anthropic, python-dotenv, apscheduler, plotly, sqlalchemy)
- Tạo `.env` (KHÔNG commit) chứa API keys: OpenAI, Anthropic (Claude), Google service account JSON path, Slack webhook URL, SMTP credentials

**Buổi chiều: Google Sheets mẫu**
- Tạo Google Sheet với cột: `id, description, example_url, output_format, model, status`
- Điền 8–10 dòng mẫu, đa dạng: có dòng PNG hợp lệ, có dòng cố tình sai URL, có dòng thiếu field — để test error handling sau này

**Buổi tối: Database schema**
```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sheet_row_id INTEGER,
    description TEXT,
    model TEXT,
    output_format TEXT,
    status TEXT DEFAULT 'PENDING',   -- PENDING, RUNNING, RETRY, SUCCESS, FAILED
    retry_count INTEGER DEFAULT 0,
    drive_url TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP
);
```
Vẽ kèm 1 sơ đồ ERD đơn giản (dùng draw.io hoặc dbdiagram.io) — chèn vào README, đây là chi tiết Tech Lead sẽ để ý vì thể hiện bạn nghĩ ở mức schema chứ không phải chỉ code.

**Deliverable cuối ngày:** Kiến trúc diagram + schema + Sheet mẫu + project structure sẵn sàng.

---

### NGÀY 2 — Automation Core

Thực hiện theo module, test độc lập từng module trước khi nối chuỗi:

1. **`sheets_reader.py`** — đọc Google Sheets qua `gspread` hoặc Sheets API, validate từng dòng (thiếu field → đánh dấu lỗi ngay, không gửi AI)
2. **`ai_generator.py`** — hàm `generate_asset(description, model)`: nếu `model == "OpenAI"` gọi OpenAI Images API, nếu `"Claude"` dùng Claude để **sinh prompt tối ưu** rồi chuyển cho model ảnh (Claude không sinh ảnh trực tiếp — ghi rõ điều này trong README để tránh bị bắt lỗi kỹ thuật, giống điểm bạn đã lưu ý về Midjourney)
3. **`retry_wrapper.py`** — decorator retry 3 lần, backoff 2s/4s/8s, sau 3 lần fail → raise lên tầng logging
4. **`drive_uploader.py`** — upload theo cấu trúc `Outputs/{date}/{format}/{filename}`
5. **`db_logger.py`** — insert/update trạng thái job vào bảng `jobs`
6. **`notifier.py`** — 2 hàm `notify_success()` và `notify_failure()`, gửi Slack (webhook) + Email (SMTP hoặc Gmail API)
7. **`main.py`** — orchestrate toàn bộ: for row in sheet → try process → except → log fail → notify

**Test case bắt buộc chạy và chụp màn hình:**
- ✅ Job thành công hoàn toàn
- ❌ Sai URL asset mẫu
- ❌ API timeout (giả lập bằng cách set timeout ngắn)
- ❌ Sai output_format (không nằm trong PNG/JPG/GIF/MP3)

**Deliverable cuối ngày:** Workflow end-to-end chạy được, có log, có notification thật trên Slack.

---

### NGÀY 3 — Prompt Engineering (Assignment 2)

> Khi bạn có thư mục asset mẫu, gửi lại cho tôi — tôi sẽ giúp phân tích style/color palette/shape cụ thể để bạn viết Prompt V1 sát hơn ngay từ đầu, đỡ mất vòng lặp.

**Quy trình đề xuất (áp dụng đúng tư duy benchmark 5 kiến trúc bạn đã làm — thử nhiều "cấu hình" prompt và so sánh có hệ thống):**

1. **Phân tích asset mẫu** trước khi viết prompt — lập bảng đặc điểm:

| Thuộc tính | Quan sát từ asset mẫu |
|---|---|
| Art style | Cartoon / Realistic / Pixel / Flat vector |
| Color palette | (liệt kê mã màu chủ đạo) |
| Góc nhìn (camera) | Isometric / Top-down / Front-facing |
| Lighting | Soft / Hard shadow / Flat |
| Background | Transparent / Solid color |
| Level of detail | Simple / Highly detailed |

2. **Viết prompt theo cấu trúc lớp** (subject → style → palette → lighting → composition → technical constraint):
```
[Subject] a small dragon icon,
[Style] flat cartoon game-asset style, clean vector shapes,
[Palette] warm orange-red gradient with dark outline,
[Lighting] soft ambient lighting, no harsh shadow,
[Composition] centered, 3/4 isometric view,
[Technical] transparent background, 512x512, icon-ready
```

3. **Bảng nhật ký lặp (bắt buộc trong tài liệu nộp):**

| Version | Prompt | Vấn đề quan sát | Điều chỉnh | Ảnh kết quả |
|---|---|---|---|---|
| V1 | ... | Quá realistic, sai style | Thêm "flat cartoon, vector style" | ảnh V1.png |
| V2 | ... | Sai bảng màu | Thêm mã màu cụ thể + "muted palette" | ảnh V2.png |
| V3 (Final) | ... | Đạt yêu cầu | — | ảnh V3.png |

4. **Bảng đánh giá so sánh với asset gốc** (dùng để chấm định lượng, thể hiện tư duy evaluation giống ML metrics bạn quen dùng):

| Tiêu chí | Điểm (1–5) | Ghi chú |
|---|---|---|
| Style consistency | | |
| Color accuracy | | |
| Shape/silhouette accuracy | | |
| Background cleanliness | | |
| Usability trong game (dễ tách nền, đúng kích thước) | | |

**Deliverable cuối ngày:** File `prompt_engineering_report.md` + toàn bộ ảnh từng version + bảng đánh giá.

---

### NGÀY 4 — Logging nâng cao, Report, README

- Hoàn thiện `daily_report.py`: query DB → tính tổng/success/fail → vẽ pie chart bằng **Plotly** (tái dùng kỹ năng dashboard của bạn) → xuất PNG hoặc HTML → đính vào email
- Thêm APScheduler chạy report lúc cuối ngày (ví dụ 23:00) độc lập với luồng xử lý chính
- Viết `README.md` đầy đủ: Installation, Configuration (.env template), Architecture diagram, How to run, Known limitations
- Test lại toàn bộ hệ thống 1 lần nữa với dữ liệu Sheet đầy đủ (10+ dòng)

**Deliverable cuối ngày:** Report tự động + README hoàn chỉnh + hệ thống ổn định.

---

### NGÀY 5 — Video, đóng gói, rà soát

**Cấu trúc video (≤10 phút) — gợi ý kịch bản theo đúng thế mạnh trình bày nghiên cứu của bạn:**

| Thời lượng | Nội dung |
|---|---|
| 0:00–0:30 | Giới thiệu ngắn gọn cách tiếp cận: "coi workflow như data pipeline có kiểm soát chất lượng" |
| 0:30–4:00 | Demo automation: trigger → Sheets → AI → Drive → DB → Slack/Email, lướt qua schema DB và log |
| 4:00–7:00 | Prompt Engineering: so sánh asset gốc vs AI, đi qua bảng V1→V2→V3, giải thích lý do điều chỉnh |
| 7:00–9:00 | Khó khăn thực tế gặp phải (API timeout, rate limit, Claude không sinh ảnh trực tiếp...) và cách xử lý (retry, backoff, tách vai trò Claude làm prompt generator) |
| 9:00–10:00 | Hướng cải tiến: queue cho khối lượng lớn, idempotency (tránh tạo lại job đã DONE), cost optimization (cache theo hash prompt), dashboard giám sát |

**Đóng gói bài nộp:**
```
LeThanhHaiHuynh_Test Submit/
├── automation/            (source code + .env.example)
├── prompt_engineering/    (report.md + toàn bộ ảnh iteration)
├── database/              (schema.sql + ERD image)
├── report_sample/         (1 daily report mẫu + chart)
├── README.md
└── video_link.txt         (hoặc file video nếu dung lượng cho phép)
```

**Trước khi gửi — checklist bắt buộc:**
- [ ] Subject email đúng format: `[AthenaStudio - Prompt Engineer] LeThanhHaiHuynh_Test Submit`
- [ ] Tên thư mục/file đúng: `LeThanhHaiHuynh_Test Submit`
- [ ] Video ≤ 10 phút, có phụ đề hoặc nói rõ ràng
- [ ] Không commit API key thật trong code (chỉ có `.env.example`)
- [ ] README chạy thử được từ đầu (không giả định môi trường sẵn có)

---

## 4. RỦI RO CẦN LƯU Ý (dựa trên phân tích đề bài)

- **Claude không sinh ảnh trực tiếp** — nếu Sheet ghi `model = Claude`, hãy dùng Claude để sinh/tối ưu prompt, sau đó gọi một model ảnh thực (OpenAI Images) để render. Giải thích rõ điều này trong README/video để tránh bị đánh giá là hiểu sai công nghệ.
- **MP3 output** không được đề bài chỉ định công cụ cụ thể — dùng TTS bất kỳ (OpenAI TTS) và ghi rõ đây là lựa chọn của bạn, không phải yêu cầu bắt buộc.
- **layer.ai** chỉ là ví dụ ("or similar tools") — không bắt buộc dùng đúng nền tảng này, có thể thay bằng công cụ bạn quen hơn.
- **Rate limit** khi Sheet có nhiều dòng — nêu trong phần "Future Improvements" là sẽ thêm queue/worker, không cần implement đầy đủ nếu thời gian hạn chế, nhưng phải *nói được* hướng giải quyết trong video.

---

## 5. ĐỊNH VỊ TRONG CV/COVER LETTER CHO VỊ TRÍ NÀY

Vì JD nghiêng về automation + AI hơn là graph ML thuần túy, khi viết cover letter/CV cho vị trí này, nhấn các dòng sau thay vì để nguyên thứ tự ưu tiên như CV Data Scientist hiện tại của bạn:
- Kinh nghiệm ERP Odoo: đã áp dụng **AI/Computer Vision low-code vào invoice-processing workflow** (500+ invoice/tháng, tiết kiệm 30% thời gian) — đây gần như là một automation project thật, hãy dẫn chứng cụ thể ngay đầu cover letter.
- Kinh nghiệm xử lý sự cố database (Odoo v18→v19 recovery, 800+ transaction, zero disruption) — chứng minh bạn hiểu giá trị của logging/backup/validation trong hệ thống thật, không chỉ lý thuyết.
- CPO certification — nhấn mạnh khả năng tự lên kế hoạch 5 ngày có milestone rõ ràng (đúng là điều bạn đang làm ở kế hoạch này).

---

*Khi bạn gửi thư mục asset mẫu, mình sẽ giúp bạn phân tích cụ thể style/màu/shape để rút ngắn số vòng lặp prompt ở Ngày 3.*
