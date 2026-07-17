# 🎬 KỊCH BẢN QUAY VIDEO SIÊU CHI TIẾT — PHIÊN BẢN TIẾNG VIỆT
*Thời lượng: Dưới 10 phút | Đọc to phần trong dấu ngoặc kép "..." | Làm theo hành động trong dấu ngoặc vuông [...]*

---

## ⏱️ PHẦN 1: MỞ ĐẦU (0:00 — 1:00)

### Hành động:
- **[0:00]** Mở trình duyệt Chrome, vào trang Github Repo: `https://github.com/danielhuynh-04/AI-Asset-Generation-Automation-Pipeline`
- **[0:05]** Để trang Github hiện rõ tên Repo và cây thư mục ở giữa màn hình.

### Lời thoại:
> "Xin chào các anh chị ban giám khảo Athena Studio.
> Em là Lê Thanh Hải Huỳnh, ứng tuyển cho vị trí **Prompt Engineer** và **Automation Engineer Intern**.
>
> Trong bài Test này, em không viết một đoạn Script tuyến tính chạy xong rồi thôi.
> Em đã thiết kế toàn bộ hệ thống dưới dạng một **Data Pipeline chuẩn Production-Ready**, nghĩa là có kiểm soát lỗi, có dự phòng rủi ro, và có khả năng chạy lại an toàn bất cứ lúc nào.
>
> Sau đây, em xin trình bày Sơ đồ Kiến trúc Hệ thống trước, rồi sẽ chạy Demo trực tiếp ngay sau đó."

---

## ⏱️ PHẦN 2: GIẢI THÍCH SƠ ĐỒ KIẾN TRÚC (1:00 — 3:00)

### Hành động:
- **[1:00]** Trên trang Github, cuộn từ từ xuống phần `README.md` cho đến khi thấy **sơ đồ Mermaid đầu tiên** (High-Level Architecture Diagram). Dừng lại. Phóng to nếu cần (Ctrl + cuộn chuột lên).
- **[1:10]** Rê chuột theo từng ô (node) trong sơ đồ khi giải thích.

### Lời thoại:
> "Đây là sơ đồ **Architecture Diagram** (Kiến trúc Hệ thống) em đã vẽ bằng mã Mermaid, nó được Github render ra trực tiếp.
>
> **(Rê chuột vào ô Google Sheets)**
> Điểm xuất phát là Google Sheets. Khi Admin nhập dữ liệu vào Sheet, module `sheets_reader` sẽ tự động quét và chỉ lấy những dòng chưa xử lý thôi. Đây chính là tính **Idempotency** — nghĩa là chạy đi chạy lại bao nhiêu lần cũng không bao giờ sinh trùng lặp ảnh, tiết kiệm 100% chi phí API.
>
> **(Rê chuột qua ô Validator)**
> Dữ liệu sau đó phải đi qua trạm kiểm duyệt Validator. Nó giúp loại bỏ hoàn toàn Rác dữ liệu — ví dụ Description bị trống, Format sai WEBP... — để ngăn hệ thống phí tiền gọi API cho những dòng chắc chắn sẽ thất bại.
>
> **(Rê chuột vào ô ThreadPoolExecutor)**
> Dữ liệu hợp lệ sẽ được đẩy vào bộ xử lý Đa Luồng **ThreadPoolExecutor** với 5 Workers. Thay vì chờ sinh xong ảnh 1 rồi mới tới ảnh 2, hệ thống gọi API sinh **5 ảnh cùng lúc**. Tốc độ tăng gấp 5 lần."

---

## ⏱️ PHẦN 3: GIẢI THÍCH CƠ CHẾ FALLBACK VÀ SƠ ĐỒ BPMN (3:00 — 4:30)

### Hành động:
- **[3:00]** Vẫn ở trang README Github. Rê chuột vào phần **Subgraph "AI Generation Engine"** trên sơ đồ Architecture.
- **[3:30]** Cuộn xuống tiếp đến sơ đồ thứ 2 — **BPMN Sequence Diagram**. Dừng lại giữa hình.

### Lời thoại:
> "**(Trỏ vào ô AI Generation Engine)**
> Đây là lõi AI. Khi gọi API sinh ảnh, mặc định hệ thống sẽ dùng **Google Gemini Imagen 3**. Nhưng tài khoản miễn phí chỉ cho 10 ảnh mỗi ngày.
> Vậy khi hết Quota thì sao? Code của em đã xử lý sẵn: nó tự động **Fallback** — tức là 'Quay xe' — sang dùng **Pollinations Flux AI** hoàn toàn miễn phí, không cần API Key. Nhờ vậy, hệ thống hoạt động liên tục 99.9% Uptime mà không bao giờ bị Crash giữa chừng.
>
> **(Rê chuột vào ô Exponential Backoff)**
> Nếu API bị lỗi mạng, hệ thống không chết ngay mà tự đợi 2 giây, rồi 4 giây, rồi 8 giây — gọi là **Exponential Backoff**. Sau 3 lần thất bại, nó mới chính thức đánh dấu FAILED.
>
> **(Cuộn xuống sơ đồ BPMN)**
> Tiếp theo là sơ đồ **BPMN** — mô hình quy trình nghiệp vụ. Các anh chị thấy em chia hệ thống thành 5 làn (Swimlanes): User, Orchestrator, AI Services, Storage, và Notifications.
> Điểm quan trọng: **Chu trình Sinh ảnh** và **Chu trình Báo cáo Hàng ngày** hoạt động hoàn toàn tách biệt. Module Báo cáo được lập trình chạy tự động lúc 23:00 đêm bằng **APScheduler**, không ảnh hưởng đến hiệu năng luồng chính."

---

## ⏱️ PHẦN 4: DEMO CHẠY PIPELINE (4:30 — 6:00)

### Hành động:
- **[4:30]** Chuyển sang cửa sổ **VS Code**. Mở Terminal (Ctrl + `).
- **[4:35]** Gõ lệnh: `.\.venv\Scripts\python src/main.py` rồi nhấn Enter.
- **[4:40]** Chờ các dòng log chạy ra. Quan sát phần có chữ `[SUCCESS]` và phần có chữ `[RETRY]` hoặc `[FAILED]`.
- **[5:10]** Khi thấy dòng `MOCK_TIMEOUT`, dùng chuột highlight (bôi đen) dòng đó.

### Lời thoại:
> "Bây giờ em chạy Demo trực tiếp hệ thống Data Pipeline này. 
> 
> **(Bôi đen dòng báo lỗi 429 bị chặn Limit hiển thị trên Terminal)**
> Khi hệ thống Đa luồng nã liên tục nhiều Job cùng lúc vào Free Tier AI, các anh chị sẽ thấy Terminal nổi lên vô số các dòng cảnh báo cảnh giác đỏ như **HTTP Error 429: Too Many Requests** hoặc **Quota Exceeded**.
> Đây không phải là Bug. Đây chính là hệ thống Đàn Hồi (Resilience) mà em cố tình giăng ra! Một Data Pipeline thực thụ phải hứng chịu được sóng gió API Rate Limit mà không bị ngắt quãng (Zero-Crash). 
> Khi bị văng lỗi 429 Timeout, hệ thống kích hoạt **Exponential Backoff**, lùi lại vài giây rồi tự gọi tiếp, hoặc quay xe Fallback sang mô hình thứ 2. 
> Nếu sau 3 lần vẫn thất bại do hạ tầng, nó không bỏ trôi dữ liệu mà sẽ bẻ lái **bắn trạng thái FAILED lật ngược trở lại Google Sheets** để Admin đối soát hai chiều, đồng thời nã Email thông báo lỗi ngay lập tức.
>
> **(Chỉ vào các dòng báo SUCCESS)**
> Nhờ tính chịu đòn lỳ lợm này, hệ thống của em vẫn âm thầm sàng lọc thành công các dòng dữ liệu hợp lệ xen kẽ trong cơn hoảng loạn, sinh ảnh xong và bốc chúng tải lên Google Drive cực kỳ an toàn."

---

## ⏱️ PHẦN 5: BẢO MẬT OAUTH 2.0 (6:00 — 6:45)

### Hành động:
- **[6:00]** Mở file `src/notifier.py` trong VS Code. Cuộn tới hàm `_get_gmail_service()`.
- **[6:15]** Dùng chuột highlight dòng chứa `InstalledAppFlow` và `gmail_token.json`.

### Lời thoại:
> "Về phần Gửi email, em đã loại bỏ hoàn toàn phương thức SMTP App Password cũ vì nó lưu mật khẩu dạng Text thuần (plaintext) rất rủi ro bị đánh cắp.
>
> **(Chỉ vào dòng InstalledAppFlow)**
> Thay vào đó, em tích hợp **Gmail API qua chuẩn OAuth 2.0**. Luồng hoạt động: lần đầu tiên chạy, hệ thống mở trình duyệt yêu cầu Admin click nút 'Cho phép'. Sau đó nó tạo ra file `gmail_token.json` lưu Refresh Token an toàn. Từ lần 2 trở đi, hệ thống tự xác thực ngầm mà không cần nhập password nữa.
>
> **(Chỉ vào file gmail_token.json và token.json)**
> Em cũng tách riêng Token cho Google Drive và Gmail theo nguyên tắc **Least Privilege** — tức là mỗi module chỉ được cấp đúng quyền hạn cần thiết, không hơn không kém."

---

## ⏱️ PHẦN 6: BÁO CÁO TỰ ĐỘNG — DAILY REPORT (6:45 — 7:30)

### Hành động:
- **[6:45]** Quay lại Terminal VS Code. Gõ lệnh: `.\.venv\Scripts\python src/daily_report.py --run-now`
- **[7:00]** Khi lệnh chạy xong, mở file HTML trong thư mục `report_sample/` bằng Chrome (kéo thả file HTML vào Chrome).
- **[7:10]** Cuộn qua từng biểu đồ trên trang HTML (Pie Chart, Bar Chart, Scatter Plot).

### Lời thoại:
> "Đây là Dashboard Báo cáo Hàng ngày. Em sử dụng thư viện **Plotly** để vẽ đồ thị tương tác.
>
> **(Rê chuột qua Biểu đồ Tròn — Pie Chart)**
> Biểu đồ này cho thấy tỉ lệ Success và Failed của toàn bộ pipeline trong ngày.
>
> **(Rê chuột qua Biểu đồ Cột — Bar Chart)**
> Biểu đồ cột thể hiện số lượng Jobs theo từng ngày, giúp Admin theo dõi xu hướng.
>
> **(Rê chuột qua Biểu đồ Phân Tán — Scatter Plot)**
> Và biểu đồ này đo Tốc độ xử lý (Execution Time) từng Job. Nếu có Job nào bất thường chậm, Admin sẽ nhìn thấy ngay.
>
> Toàn bộ bảng Dashboard HTML này được nhúng tự động vào Email gửi cho Admin lúc 23:00 hằng ngày."

---

## ⏱️ PHẦN 7: PROMPT ENGINEERING — BÀI 2 (7:30 — 9:00)

### Hành động:
- **[7:30]** Mở file `prompt_engineering/prompt_engineering_report.md` trong VS Code hoặc trên Github.
- **[7:45]** Cuộn tới phần bảng Ma Trận Phân Tích (Art Style, Colors, Camera...).
- **[8:00]** Cuộn tới phần Ảnh so sánh V1 → V2 → V3 của từng loại Asset (Characters, Balls, Buttons...).
- **[8:30]** Dừng lại ở ảnh V3 Final đẹp nhất.

### Lời thoại:
> "Chuyển sang Bài 2 — Prompt Engineering.
>
> **(Chỉ vào bảng Ma Trận)**
> Để sinh ra Asset 2D phong cách Bingo Studio, em đã phân tích mẫu gốc thành 5 chiều: Art Style, Hex Colors, Camera Angle, Lighting, và Detail Level. Từ đó em xây dựng cấu trúc Prompt dạng Modular.
>
> **(Cuộn qua các ảnh V1 → V2 → V3)**
> Ở Version 1, màu sắc bị lẫn lộn và thiếu đồng nhất. Em đã khắc phục ở V2 bằng cách thêm từ khoá chính xác 'Monochromatic Colorway'. Đến Version 3, kết quả đạt độ sắc nét cao nhất, có thể thay trực tiếp vào Game Engine mà không cần chỉnh sửa thêm.
>
> **(Dừng ở ảnh V3)**
> Tất cả các vòng lặp đều được ghi nhật ký đầy đủ: Prompt đã dùng, Vấn đề gặp phải, Cách khắc phục, và Điểm đánh giá định lượng theo thang 1 đến 5."

---

## ⏱️ PHẦN 8: KẾT LUẬN VÀ ĐỀ XUẤT (9:00 — 10:00)

### Hành động:
- **[9:00]** Quay lại trang Github Repo. Cuộn xuống bảng **Known Limitations & Future Work** trong README.
- **[9:30]** Cuộn lên đầu trang Github để kết thúc ở tên Repo.

### Lời thoại:
> "**(Chỉ vào bảng Limitations)**
> Em nhận thức rõ giới hạn hiện tại. SQLite chỉ phù hợp cho một người dùng. Queue nội bộ sẽ không chịu nổi khi có hàng ngàn Jobs.
>
> Nếu có ngân sách trong môi trường Production, em đề xuất 2 hướng cải tiến:
> Một là đẩy hàng đợi lên **Celery kết hợp Redis** để xử lý phân tán.
> Hai là áp dụng **Cache bằng SHA-256 Hash** — nếu Prompt giống nhau thì bỏ qua không sinh lại, tiết kiệm triệt để phí API.
>
> **(Cuộn lên đầu trang)**
> Tuy dự án quy mô còn nhỏ, nhưng em mong nó thể hiện được tư duy hệ thống (**System Mindset**) của em khi tiếp cận mọi bài toán kỹ thuật.
> Em rất mong có cơ hội học hỏi và phát triển tại Athena Studio. Xin cảm ơn các anh chị đã lắng nghe!"

---

## ✅ CHECKLIST TRƯỚC KHI BẤM NÚT GHI HÌNH

| # | Hạng mục | Kiểm tra |
|---|---|---|
| 1 | Mở sẵn trang Github Repo trên Chrome | ☐ |
| 2 | Mở sẵn VS Code với Terminal (đã activate `.venv`) | ☐ |
| 3 | Google Sheet có dữ liệu mẫu (bao gồm dòng `MOCK_TIMEOUT`) | ☐ |
| 4 | File `credentials.json`, `token.json`, `gmail_token.json` đã có sẵn | ☐ |
| 5 | Thư mục `report_sample/` có ít nhất 1 file HTML mẫu | ☐ |
| 6 | Micro + Phần mềm ghi màn hình (OBS Studio / Loom) đã sẵn sàng | ☐ |
| 7 | Đọc thử kịch bản 1 lần trước khi ghi hình chính thức | ☐ |
