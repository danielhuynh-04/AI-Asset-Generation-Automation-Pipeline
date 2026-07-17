# 🎬 KỊCH BẢN VIDEO THUYẾT TRÌNH - ATHENA STUDIO INTERN TEST
*Thời lượng tối đa: 10 phút. Mục tiêu: Thể hiện phong thái tự tin, khiêm nhường nhưng am hiểu sâu sắc về kiến trúc hệ thống (System Mindset).*

---

## 1. Mở đầu (0:00 - 1:00)
**[Hiển thị: Slide Giới thiệu / Portfolio]**
- Xin chào các anh chị ban giám khảo Athena Studio. Em là Lê Thanh Hải Huỳnh, ứng viên cho vị trí Prompt Engineer / Automation Engineer Intern.
- Với định hướng phát triển bản thân thành một Kỹ sư Tự động hóa Dữ liệu (Data Automation Engineer), em không tiếp cận bài Test này như một kịch bản code chạy một lần (one-off script). 
- Thay vào đó, em đã thiết kế toàn bộ luồng xử lý này như một **Mạng lưới Data Pipeline chuẩn Production-Ready**, nơi mọi nút thắt (bottlenecks) đều được dự phòng rủi ro kỹ lưỡng.

---

## 2. Phần A - Kiến trúc Automation (1:00 - 4:00)
**[Hiển thị: Mở hình ảnh Architecture Diagram trên Github hoặc Miro]**
- Để giải quyết bài toán tự động sinh Asset, hệ thống của em vận hành qua 5 lõi chính. Thay vì chờ mòn mỏi sinh từng ảnh, em áp dụng **ThreadPoolExecutor (Xử lý Đa Luồng)** để gọi API sinh hàng chục ảnh cùng lúc.
- **Tính toán Edge Case 1 (Lỗi Database Lock):** Khi lưu kết quả từ nhiều luồng vào SQLite, lỗi Deadlock rất dễ xảy ra. Em đã tinh chỉnh SQLAlchemy bằng cờ `check_same_thread=False` để tạo ra một State Machine an toàn tuyệt đối.
- **Tính toán Edge Case 2 (Sập API):** Nếu Google Gemini hết Quota hoặc bị lỗi mạng thì sao? Code của em sẽ tự động kích hoạt **Cơ chế Fallback (Quay xe) sang ChatGPT (Pollinations Flux AI)**. Điều này giúp hệ thống đạt Uptime gần như tuyệt đối mà không cần can thiệp thủ công.
- **Bảo vệ Idempotency (Tính Lặp An Toàn):** Pipeline của em quét Sheet và bỏ qua các Jobs đã đánh dấu `DONE`. Admin có thể ngắt điện giữa chừng, khi bật lại, hệ thống sẽ chạy tiếp dòng chưa xong chứ không bao giờ sinh trùng ảnh gây tốn tiền API.

---

## 3. Phần A - Demo & Bảo mật (4:00 - 6:00)
**[Hiển thị: Mở Terminal VS Code, Gõ lệnh `python src/main.py`]**
- Dạ, sau đây em xin phép chạy Demo. Trong Google Sheet, em có cài cắm từ khoá `MOCK_TIMEOUT` ở một dòng cố định.
- *(Chỉ vào màn hình Terminal)* Như các anh chị thấy, khi bắt gặp lỗi Timeout, hệ thống không Crash mà kích hoạt bộ điếm giờ (Exponential Backoff): tự chờ 2 giây, rồi thử lại 4 giây. Sau 3 lần thất bại, nó mới đánh dấu FAILED và gửi Cảnh báo thất bại Tức thời.
- **Bảo mật Enterprise Zero-Trust:** Về phần gửi Cảnh báo và Báo cáo qua Email, em KHÔNG SỬ DỤNG Mật khẩu Ứng dụng (App Password) cấp qua giao thức SMTP cũ vì cực kỳ rủi ro rò rỉ. Thay vào đó, em ứng dụng luồng **Google OAuth 2.0 Web Consent (Gmail API)**. Admin chỉ cần click Allow trên trình duyệt ở lần chạy đầu tiên, script sẽ giữ một Token an toàn và tự động chạy ngầm mãi mãi về sau. 

---

## 4. Phần A - Daily Report (6:00 - 7:00)
**[Hiển thị: Gõ lệnh `python src/daily_report.py --run-now`, mở file HTML bằng trình duyệt]**
- Cuối cùng, thay vì gửi một núi Log cứng nhắc, em xây dựng module Analytics riêng biệt chạy bằng toán tử **APScheduler** vào đúng 23:00 đêm hằng ngày.
- *(Chỉ vào Dashboard HTML trên trình duyệt)* Báo cáo xuất ra dưới dạng đồ thị Interactive Plotly (với đầy đủ biểu đồ Tròn, Cột, Scatter) để đo lường tỷ lệ Thành công và Thời gian Thực thi (Execution Time). Dashboard này được nhúng tự động gửi thẳng vào hộp thư Giám đốc.

---

## 5. Phần B - Chiến lược Prompt Engineering (7:00 - 9:00)
**[Hiển thị: Mở file prompt_engineering_report.md lên cuộn]**
- Chuyển sang Assignment 2, để Gen ra những chiếc Asset Game Bingo sắc nét và không bị "ảo", em đã lập bảng ma trận phân tích 5 tiêu chí: Art Style, Hex Colors, Camera Angle, Lighting và Detail Level.
- Từ đó, mẫu Prompt chuẩn của em luôn tuân theo cấu trúc Modular:
  `[Subject] + [Style: cel-shading] + [Lighting: inner glow] + [Camera: straight-on] + [Format: transparent background]`.
- *(Chỉ vào các bức ảnh quá trình đổi Version)* Ở phiên bản V1, màu bị lẫn lộn. Em đã fix bằng cách dùng Exact Keyword "Monochromatic Colorway", đến V3 thì asset đạt độ hoàn thiện cao nhất có thể thay trực tiếp vào Game Engine.

---

## 6. Tổng kết & Đề xuất Cải tiến (9:00 - 10:00)
**[Hiển thị: Slide Cảm ơn / Mở lại trang chủ Code Github]**
- Em nhận thức rằng phiên bản hiện tại vãn có giới hạn. Nếu có dự án ngân sách lớn, em đề xuất đưa Queue Worker (như Celery Redis) vào thay thế ThreadPool và triển khai Caching (SHA256 Hash Prompts) để tối ưu chi phí sinh ảnh trùng lặp.
- Lời cuối, bài Test này phản ánh toàn vẹn tư duy của em: Viết code quy mô công nghiệp (Production-ready), dễ bảo trì và bám sát giá trị nghiệp vụ.
- Rất mong có cơ hội thực tập, học hỏi tại Athena Studio để hoàn thiện bản thân vươn tầm chuyên gia. Cảm ơn các anh chị đã lắng nghe.
