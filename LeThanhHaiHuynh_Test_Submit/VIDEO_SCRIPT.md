# 🎙️ KỊCH BẢN THUYẾT TRÌNH (Assignment 3)
## Vị trí: Prompt Engineer / Automation Engineer Intern
**Ứng viên:** Lê Thanh Hải Huỳnh (Daniel) | **Thời lượng dự kiến:** 7-8 phút

---

## 🎬 TIPS QUAY VIDEO TRƯỚC KHI BẮT ĐẦU
1. **Chia đôi màn hình:** Một bên mở Slides/Code, một bên mở Terminal hoặc hình ảnh để demo trực quan.
2. **Setup:** Bật mic rõ ràng, có Facecam là điểm cộng rất lớn (mang lại sự tự tin).
3. **Mindset:** Hãy nói như mặt đối mặt với Tech Lead/Product Manager. Đừng chỉ đọc slide, hãy "kể một câu chuyện" về cách bạn tiếp cận và giải quyết vấn đề.

---

## ⏱️ KỊCH BẢN CHI TIẾT (Theo timeline)

### 1. Introduction & Objectives (0:00 - 1:00)
**[Hình ảnh hiển thị: Mở đầu bằng Title hoặc README repo]**

**📝 Kịch bản:**
> "Xin chào Ban Tuyển Dụng Athena Studio, mình là Daniel Huỳnh. Hôm nay mình rất vui được trình bày về giải pháp cho bài test Vị trí Prompt Engineer & Automation Engineer Intern.
> 
> Thay vì chỉ viết một Python Script đơn giản chạy 1 phòng lặp, chiến lược của mình là tiếp cận bài toán này dưới góc độ của một **Data Pipeline Engineering**. Mình muốn xây dựng một hệ thống Tự động hóa không chỉ chạy được, mà còn phải: kiểm soát được lỗi, an toàn dữ liệu, chạy đa luồng nhanh chóng và tự động báo cáo.
>
> *(Chỉ vào Gantt Chart trong README)* 
> Để kiểm soát tiến độ trong 5 ngày, mình đã tự lập một **Gantt Chart Execution Plan**. Ở đây mọi thứ được chia Milestone cực kì rõ ràng từ Design, Logic Core, đến Prompting và Report. Tư duy Quản lý dự án (PM Thinking) và Quản lý Rủi Ro (Risk Management) là xương sống để dự án này không đi chệch hướng.
>
> Mình xin phép chia bài thuyết trình thành hai phần chính: Part A - Kiến trúc Automation Workflow và Part B - Chiến lược Prompt Engineering."

---

### 2. Part A: Automation Workflow Architecture (1:00 - 3:30)
**[Hình ảnh hiển thị: Mở `README.md` phần sơ đồ Workflow Architecture hoặc biểu đồ ERD Diagram]**

**📝 Kịch bản:**
> "Ở phần đầu tiên, Kiến trúc luồng tự động hóa. Khi có một request từ Google Sheet, hệ thống mình thiết kế sẽ đi qua 5 module chính:
>
> **1. Validate (Kiểm duyệt):** Hệ thống không đưa rác vào AI. Bất kỳ dòng nào sai định dạng Format, hoặc thiếu Description sẽ bị log lại và chặn ngay từ vòng gửi xe.
> **2. AI Generation:** Ở bước này, để giải quyết bài toán Rate Limit của free-tier, mình đã thiết lập một **Fallback Mechanism**. Ví dụ: Mặc định tối ưu prompt bằng Gemini Pro, nhưng nếu sập API hay hết Quota, hệ thống sẽ ngầm fallback chuyển sang mạng ChatGPT thông qua Pollinations Text API hoàn toàn miễn phí, giữ Uptime 99.9%.
> **3. Multithreading (Xử lý Đa luồng):** Mình không để chương trình chạy tuần tự. Bằng cách dùng `ThreadPoolExecutor(max_workers=5)`, mình gọi 5 luồng API song song. Tốc độ render hàng trăm tấm ảnh tăng lên gấp 5 lần, giải quyết điểm nghẽn cổ chai (I/O Bound).
> **4. Tracking & Notification:** Toàn bộ trạng thái (RUNNING, FAILED, SUCCESS) được ghi vào cơ sở dữ liệu SQLite *chuẩn Thread-Safe*. Sau khi hoàn tất sẽ có thông báo đẩy trực tiếp qua Slack. 
>
> _(Bạn có thể mở nhanh Terminal gõ lệnh `python src/main.py` để họ thấy các luồng log đang chạy lên màn hình)_."

---

### 3. Part B: Prompt Engineering Strategy (3:30 - 6:00)
**[Hình ảnh hiển thị: Mở thư mục `iterations` chiếu các ảnh vòng lặp V1->V3, và file report]**

**📝 Kịch bản:**
> "Chuyển sang Assignment 2, Chiến lược Prompt Engineering. Giống như tư duy xử lý Data, mình không viết prompt theo cảm hứng, mà dùng phương pháp tiếp cận có hệ thống gọi là **Modular 7-Layer Architecture** (chuẩn Google/NVIDIA).
> 
> Mình chia 1 prompt ra làm 7 lớp thay thế được: `[SUBJECT]`, `[STYLE]`, `[PALETTE]`, `[LIGHTING]`, `[COMPOSITION]`, `[TECHNICAL]` và `[NEGATIVE]`. 
> 
> Dựa trên việc phân tích trực tiếp Asset của con game Bingo, thay vì nói 'hãy vẽ màu đỏ', mình gắn cứng mã HEX như `#F44336`. Yếu tố khác biệt nhất mình tự nhận thấy giữa ảnh AI bình thường và Asset Game chuyên nghiệp nằm ở LAYER `[LIGHTING]` (Ánh sáng). Mình áp dụng các kĩ thuật Three-point studio lighting, hoặc Specular highlights để biến một hình tròn tĩnh 2D trở thành một quả bóng 3D Glossy.
>
> Nhờ bảng đánh giá Likert Scale 5 góc độ, mình cô lập nguyên nhân ở từng lần thay đổi, giúp ảnh từ version 1 đến version 3 Cải thiện chất lượng hơn 100%, có thể overlay trực tiếp ngay vào UI mobile game."

---

### 4. Challenges & Solutions (6:00 - 7:30)
**[Hình ảnh hiển thị: Mở `main.py` đoạn try catch hoặc `db_logger.py`]**

**📝 Kịch bản:**
> "Trong quá trình xây dựng, mình có gặp hai thách thức kỹ thuật lớn nhất:
> 
> **Thứ nhất: Sự cố I/O Bound và SQLite DB Lock.** Khi chạy đa luồng để gọi AI cho nhanh, Database SQLite bị treo do ghi đồng thời quá nhiều. Mình đã dự báo rủi ro (Risk) này từ lúc lên sơ đồ kiến trúc, nên giải pháp là set `check_same_thread=False` và cấp timeout `15s` trên SQLAlchemy Engine, biến DB trở nên hoàn toàn Thread-Safe.
>
> **Thứ hai: Lỗi Timeout và ngỏm API.** Rủi ro lớn nhất của hệ thống Automation tự chạy ban đêm là đứt mạng hoặc chết API. Mình đã chủ động quản trị rủi ro bằng cách tự viết một `retry_wrapper` (Decorator) tự động Back-off lùi thời gian thử lại 2s, 4s, 8s, kết hợp Fallback Model sang ChatGPT miễn phí. Nhờ quản lý tốt các rủi ro này, pipeline luôn đạt chuẩn Uptime 99.9%."

---

### 5. Future Improvements & Conclusion (7:30 - 8:30)
**[Hình ảnh hiển thị: Mở `daily_report.py` HTML hiển thị Dashboard hoặc trỏ chuột vào mục Future Work trên Github]**

**📝 Kịch bản:**
> "Về hướng đi tương lai (Future work), nếu đưa dự án này lên Production (môi trường thực tế) với hàng ngàn lệnh sinh ảnh mỗi ngày, mình đề xuất 2 cải tiến:
> 1. Dùng hàng đợi (Queue Worker) theo chuẩn Celery + Redis thay vì ThreadPool trong script.
> 2. Tính mã băm `SHA256 Hash` cho mỗi câu Description, đưa vào Caching. Nếu Designer gõ lại 1 yêu cầu cũ đã gen, hệ thống tự load ảnh có sẵn thay vì tốn tiền gọi AI thêm lần nữa.
>
> Tổng kết lại, sản phẩm của mình không dừng lại ở một script chạy API, mà là một hệ thống Pipeline tự động mạnh mẽ, mở rộng được và tài liệu hóa chuẩn chỉnh. Hi vọng cách tiếp cận kỹ thuật này phù hợp với văn hóa Data-driven và Engineering Excellence của Athena Studio.
> 
> Cảm ơn Ban Tuyển Dụng đã lắng nghe. Mình rất mong đợi cơ hội được trao đổi sâu hơn ở vòng phỏng vấn tiếp theo!"

---
> 🎯 **Chúc bạn quay video thành công rực rỡ, nói to rõ, nhấn nhá đúng nhịp!**
