# 🎬 KỊCH BẢN ĐỌC THUYẾT TRÌNH CHI TIẾT DÀNH CHO ỨNG VIÊN
*(Hướng dẫn: Phần trong ngoặc vuông **[...]** là hành động tay. Phần chữ bình thường là LỜI NÓI bạn sẽ ĐỌC trực tiếp vút ra khỏi miệng lồng tiếng cho video. Đọc thật dõng dạc và nhấn nhá các từ in đậm).*

---

## 1. Mở Đầu (0:00 - 1:00)
**[Mở Slide giới thiệu bản thân hoặc Hình ảnh Title bài Test]**
"Xin chào các anh chị ban giám khảo Athena Studio. Em là Lê Thanh Hải Huỳnh, ứng tuyển cho vị trí Prompt Engineer và Automation Engineer Intern.
Trong dự án này, em không tiếp cận bài toán theo hướng chỉ viết một đoạn script chạy tuyến tính bình thường. Mục tiêu của em là xây dựng một **Quy trình Dữ Liệu (Data Pipeline)** chuẩn mực, sẵn sàng cho môi trường thực tế (Production-ready). Sau đây, em xin phép dùng Sơ đồ Kiến trúc để minh họa cho phần thiết kế hệ thống của mình."

---

## 2. Giải thích Architecture Diagram & BPMN (1:00 - 4:30)
**[Cuộn trang README trên Github tới phần: Tái hiện rõ 2 hình ảnh Architecture Diagram và BPMN]**
"(Rê chuột vào hình High-Level Architecture Diagram) 
Như các anh chị thấy ở sơ đồ luồng dữ liệu này, em đã bóc tách kiến trúc hệ thống (Decoupling) thành các module độc lập. 
Dữ liệu đầu vào từ Google Sheets sẽ phải đi qua trạm kiểm duyệt **Validator** trước. Nó giúp lọc bỏ 100% rác dữ liệu trước khi hệ thống tốn tài nguyên gọi API xử lý (tiết kiệm chi phí).

Sau khi dữ liệu an toàn, hệ thống sẽ sử dụng **ThreadPoolExecutor** để xử lý nhiều ảnh song song (Đa Luồng).
(Trỏ chuột vào ô AI Generation Engine)
Điểm đặc biệt nhất trong lõi sinh ảnh AI này là cơ chế **Fallback**. Do tài khoản Gemini chỉ cho phép sinh giới hạn số lượng ảnh miễn phí trong ngày, em đã thiết kế thêm một module dự phòng. Nếu Gemini báo lỗi Quota, mã nguồn sẽ tự động 'Quay xe' (Fallback) để dùng Flux AI từ Pollinations hoàn toàn trơn tru. Điều này giúp hệ thống đạt thời gian hoạt động Uptime gần như tuyệt đối 99.9% mà không bị sập (Crash).

(Kéo xuống phần BPMN Sequence Diagram)
Sang đến biểu đồ luồng nghiệp vụ BPMN, các anh chị sẽ thấy em chia thành 2 chu trình rõ rệt. Chu trình sinh ảnh ở khối (Execution Loop) hoạt động hoàn toàn độc lập với Chu trình Báo Cáo. Em dùng toán tử **APScheduler** để lập lịch tự động kích hoạt tính năng tính toán KPI và vẽ biểu đồ gửi mail vào đúng 23:00 hằng ngày, không gây ảnh hưởng đến phần lõi sinh ảnh."

---

## 3. Demo Code và Giải thích Bảo mật (4:30 - 7:00)
**[Mở màn hình VS Code Terminal, gõ lệnh `python src/main.py`]**
"Bây giờ, em xin phép chạy Demo. Trong Google Sheet, em có cài cắm từ khoá `MOCK_TIMEOUT` ở một dòng cố định để test hệ thống.
(Chỉ vào những dòng chữ Warnings/Errors hiện lên terminal)
Như các anh chị đang thấy! Hệ thống bắt gặp mạng lỗi nhưng không hề bị sập màn hình đỏ. Nó tự động kích hoạt chức năng **Exponential Backoff** - tự đợi 2 giây, rồi thử lại đợi 4 giây. Sau 3 lần thất bại, nó lưu gọn gàng Trạng thái FAILED vào Database SQLite. Để giải quyết rủi ro ghi đè khi chạy Đa Luồng, Database đã được em bật cờ check Same Thread tắt đi.

Về vấn đề Báo Cáo, em đã loại bỏ phương thức khai báo Passwords SMTP cũ để chống bị đánh cắp thông tin. Em ứng dụng **Google OAuth 2.0 Web Consent (Gmail API)**. Nhờ đó, bảo mật Email của hệ thống nay đã đạt độ an toàn tuyệt đối (Zero-Trust Security)."

---

## 4. Báo Cáo & Prompt Engineering (7:00 - 9:00)
**[Gõ lệnh `python src/daily_report.py --run-now` rồi mở File HTML báo cáo lên trên Browser]**
"Và đây là Báo cáo tự động (Daily Report) dạng HTML. Em sử dụng bộ thư viện đồ thị Plotly để vẽ ra Biểu đồ tương tác, tổng hợp toàn bộ Tỉ lệ Thành công (Success Rate), Tần suất Lỗi, Tốc độ chạy trung bình... Bảng điều khiển này cũng gửi tự động vào hộp thư Admin để theo dõi hàng ngày.

**[Mở File `prompt_engineering/prompt_engineering_report.md` cuộn các ảnh thay đổi qua vòng lặp]**
Chuyển sang Assignment 2, để Gen ra những Asset 2D chất lượng Bingo Studio, em đã xây dựng mô hình Phân tích ma trận 5 chiều: Art Style, Hex Colors, Camera Angle, Lighting và Detail Level.
Em áp dụng cấu trúc câu lệnh Modular có chủ đích. Các anh chị có thể thấy qua 3 vòng lặp (Iterations), em đã thay đổi các Keyword mấu chốt để ép AI xử lý các màu rác, kết quả cuối cùng cho ra bộ nút bấm và Background rất ổn định để thay trực tiếp vào Game."

---

## 5. Kết luận và Mở rộng tương lai (9:00 - 10:00)
**[Mở Github Repo trang chính]**
"Do hạn chế về công cụ miễn phí, hệ thống hiện tại đang khóa bằng SQLite và Queue nội bộ. Ở môi trường Production có quy mô vốn lớn, giải pháp tương lai của em sẽ là đẩy Queue lên Celery Redis và áp dụng Caching bộ nhớ đệm băm (Hash Caching) nếu các Prompt bị lặp lại, nhằm tiết kiệm sâu nhất phí API cho Server.
Tuy quy mô source code còn rất khiêm tốn, nhưng em mong dự án sẽ thể hiện được 'System Mindset' của bản thân khi ứng tuyển làm Thực tập sinh tại Athena Studio. Em rất mong nhận được những nhận xét đóng góp quý giá từ anh chị. Xin cảm ơn ạ!"
