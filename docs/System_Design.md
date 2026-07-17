# 🏛️ System Design & Architecture
*Athena Studio - AI Asset Generation Automation Pipeline*

## 1. High-Level Architecture Diagram
Đây là kiến trúc luồng dữ liệu chính của AI Asset Pipeline. Hệ thống được thiết kế với tư duy Module hóa cao (Decoupled architecture) và có khả năng phục hồi lỗi (Fault-tolerant).

```mermaid
graph TD
    %% Define Nodes
    A[Google Sheets<br>Data Input] -->|Read Pending Rows| B(src/sheets_reader.py);
    B -->|Raw Rows| C{src/validator.py};
    
    C -- Invalid --> D[src/db_logger.py<br>Mark FAILED];
    C -- Valid --> E(src/main.py<br>ThreadPoolExecutor);
    
    E -->|Dispatch| F[src/ai_generator.py];
    
    %% AI Generator Sub-Logic
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
    
    %% Async Reporting
    Q((APScheduler)) -.->|Trigger 23:00| R[src/daily_report.py];
    M -.->|Query Stats| R;
    R -->|Plotly Charts| S[HTML Dashboard];
    S --> P;
```

## 2. BPMN Workflow (Swimlane Diagram)
Quy trình nghiệp vụ chi tiết được mô phỏng dưới dạng Swimlanes để thể hiện rõ trách nhiệm của từng phân hệ (Separation of Concerns).

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

## 3. Core Design Principles Applied
1. **Idempotency (Tính luỹ đẳng):** Khả năng chạy lại pipeline nhiều lần mà không tạo ra side-effect (bot chỉ đọc và xử lý những dòng chưa có trạng thái `DONE` hoặc `FAILED`).
2. **Graceful Degradation:** Hệ thống tự động hạ cấp xuống dịch vụ miễn phí (Pollinations AI/ChatGPT) để duy trì luồng công việc thay vì Crash khi dịch vụ trả phí gặp vấn đề.
3. **Concurrency without Deadlocks:** Ứng dụng ThreadPool để xử lý I/O Bound song song, nhưng vẫn đảm bảo tính kiên định của Database bằng cấu hình SQLAlchemy phù hợp.
4. **Decoupling Validation from Execution:** Validator kiểm soát độc lập 100% rác dữ liệu trước khi tốn tiền gọi API.
