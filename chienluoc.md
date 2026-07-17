Mình nghĩ với hồ sơ của bạn, **đừng tiếp cận bài test như một Prompt Engineer**.

Hãy tiếp cận nó như một **Data Pipeline Engineer xây dựng hệ thống AI Automation**.

Đây là điểm khác biệt lớn nhất của bạn so với đa số ứng viên.

---

# Tại sao?

Nếu nhìn vào CV của bạn, gần như toàn bộ kinh nghiệm đều xoay quanh **pipeline dữ liệu**, không phải web development.

Bạn có:

* Python
* SQL
* Machine Learning
* Graph Neural Network
* Feature Engineering
* Data Validation
* Visualization
* ERP Workflow
* BPMN
* Project Management (CPO)

Thực ra đây lại là một lợi thế.

Automation Workflow thực chất cũng là một **pipeline**.

Ví dụ:

```
Google Sheet

↓

Validate

↓

AI

↓

Store

↓

Database

↓

Visualization

↓

Report
```

Pipeline này không khác nhiều so với pipeline GNN của bạn.

Ví dụ project Dengue của bạn

```
Raw CSV

↓

Cleaning

↓

Feature Engineering

↓

Graph Construction

↓

Training

↓

Evaluation

↓

Visualization

↓

Report
```

Khác nhau chỉ ở domain.

---

# Cách mình muốn bạn nghĩ

Đừng nghĩ

> "Mình đang làm Automation."

Hãy nghĩ

> "Mình đang xây dựng một Data Pipeline có AI."

Đây là mindset của Data Engineer.

---

# MỤC TIÊU DỰ ÁN

Mình sẽ đặt tên luôn.

> **AI Asset Generation Automation Pipeline**

---

# Kế hoạch tổng thể

```
Planning

↓

Architecture

↓

Environment

↓

Core Modules

↓

Integration

↓

Testing

↓

Documentation

↓

Presentation
```

---

# GIAI ĐOẠN 1

## Requirement Analysis

Thời gian

> 3 giờ

Đây là phần quan trọng nhất.

Nếu phân tích sai

↓

5 ngày sau vẫn sai.

---

## Công việc

Tạo thư mục

```
docs/
```

Trong đó tạo

```
Requirement_Analysis.md
```

Viết

---

### Objective

Ví dụ

```
Build an end-to-end AI automation workflow capable of:

Reading Google Sheets

Generating AI assets

Saving outputs

Logging

Reporting

Notification
```

---

### Functional Requirements

Ví dụ

```
FR-01

Read Google Sheet

FR-02

Validate Input

FR-03

Generate Asset

FR-04

Upload Google Drive

FR-05

Slack Notification

FR-06

Email Notification

FR-07

Logging

FR-08

Daily Report
```

---

### Non-functional

Ví dụ

```
Retry

Scalable

Logging

Reliable

Maintainable
```

---

Đây là cách Project Manager thường viết.

Bạn có CPO.

Hãy tận dụng.

---

# GIAI ĐOẠN 2

## System Design

Thời gian

4 giờ

---

Bạn có học BPMN.

Đừng chỉ vẽ flowchart.

Hãy vẽ

* Use Case

* BPMN

* Architecture

* Sequence Diagram

Ví dụ

```
User

↓

Google Sheet

↓

Automation Service

↓

AI

↓

Database

↓

Drive

↓

Slack

↓

Email
```

---

## Data Flow

Bạn xuất thân Data.

Đây là thế mạnh.

Ví dụ

```
Raw Input

↓

Validation

↓

Transformation

↓

Generation

↓

Storage

↓

Visualization
```

---

## Database

Bạn từng dùng

* SQL Server

* pgAdmin

* PowerDesigner

Nên hãy thiết kế Database đẹp.

Ví dụ

```
jobs

notifications

reports
```

Có ERD.

---

# GIAI ĐOẠN 3

Environment

Thời gian

2 giờ

---

Cài

Python

↓

Virtual Environment

↓

Git

↓

Requirements

↓

.env

↓

Google API

↓

OpenAI API

↓

Slack

↓

SMTP

---

Đến đây

chưa viết code.

---

# GIAI ĐOẠN 4

Module Design

Đây mới là lúc code.

---

Không code main.py.

Chia module.

```
Reader

↓

Validator

↓

Generator

↓

Uploader

↓

Logger

↓

Reporter

↓

Notifier
```

---

Bạn sẽ thấy

Nó rất giống pipeline ML.

---

# GIAI ĐOẠN 5

Input Validation

Đây là thứ Data Scientist rất mạnh.

Ví dụ

```
description

NULL

↓

Reject
```

```
Output Format

PNG

JPG

GIF

MP3

↓

OK
```

```
Model

OpenAI

Claude

↓

OK
```

---

Bạn từng làm

Data Leakage

Validation

Sanity Check

Hãy áp dụng.

---

# GIAI ĐOẠN 6

AI Generation

Module

```
generate_asset()

```

Không cần quan tâm Google Drive.

Chỉ cần

Input

↓

Output

---

# GIAI ĐOẠN 7

Storage

```
Output

↓

Google Drive

↓

URL

↓

Database
```

---

# GIAI ĐOẠN 8

Logging

Đây là thế mạnh Data.

Đừng chỉ log

Success

Fail

Hãy log

```
Pending

Running

Retry

Completed

Failed

Execution Time

Model

Prompt

Output URL

Error
```

---

# GIAI ĐOẠN 9

Analytics

Đây là phần bạn sẽ vượt nhiều ứng viên.

Bạn từng dùng

Plotly

Mapbox

Visualization

Thì Report nên đẹp.

Ví dụ

```
Pie

Success Rate
```

```
Bar

Daily Jobs
```

```
Timeline

Execution
```

```
Failure Trend
```

---

# GIAI ĐOẠN 10

Prompt Engineering

Đừng coi đây là viết Prompt.

Hãy coi

đây là

Experiment.

Giống hệt ML.

Ví dụ

```
Experiment 1

↓

Evaluation

↓

Modify

↓

Experiment 2

↓

Evaluation

↓

Experiment 3
```

Giống benchmark

5 GNN architectures.

---

# GIAI ĐOẠN 11

Testing

Bạn từng làm

Sanity Check

Permutation Test

Validation

Hãy tạo

```
Unit Test

↓

Integration Test

↓

System Test
```

Ví dụ

| Test              | Kỳ vọng              |
| ----------------- | -------------------- |
| Sai URL           | Log lỗi, không crash |
| Thiếu description | Skip và ghi log      |
| API timeout       | Retry rồi thông báo  |
| Sai output format | Validation từ đầu    |

---

# GIAI ĐOẠN 12

Documentation

Đây là nơi CV của bạn mạnh nhất.

Bạn từng

* Research Proposal
* Thesis
* Kaggle Documentation
* SOP
* BPMN

Hãy viết giống paper.

```
Introduction

↓

Architecture

↓

Methodology

↓

Implementation

↓

Evaluation

↓

Future Work
```

---

# GIAI ĐOẠN 13

Presentation

Bạn từng

* Defense
* Research Presentation

Đừng quay video kiểu demo.

Hãy quay kiểu

Conference Presentation.

```
Problem

↓

Architecture

↓

Implementation

↓

Results

↓

Discussion

↓

Future Work
```

Nhà tuyển dụng sẽ thấy rõ tư duy kỹ thuật của bạn.

---

# Gantt Chart (5 ngày)

| Công việc                      | Ngày 1 | Ngày 2 | Ngày 3 | Ngày 4 | Ngày 5 |
| ------------------------------ | :----: | :----: | :----: | :----: | :----: |
| Requirement Analysis           |  ████  |        |        |        |        |
| System Architecture & BPMN     |  ████  |        |        |        |        |
| Environment & API Setup        |   ███  |    █   |        |        |        |
| Database Design                |   ███  |    █   |        |        |        |
| Google Sheets & Validation     |        |  ████  |        |        |        |
| AI Generation Module           |        |   ███  |   ██   |        |        |
| Google Drive Integration       |        |   ██   |   ██   |        |        |
| Logging & Database             |        |   ██   |   ███  |        |        |
| Slack & Email Notification     |        |        |   ███  |        |        |
| Prompt Engineering Experiments |        |        |  ████  |    █   |        |
| Daily Report & Visualization   |        |        |        |  ████  |        |
| Integration Testing            |        |        |        |   ███  |    █   |
| Documentation (README, Report) |        |        |    █   |   ███  |   ██   |
| Video Presentation             |        |        |        |        |   ███  |
| Final Review & Submission      |        |        |        |        |   ███  |

## Điều quan trọng nhất

Bạn **không cần chứng minh mình là một Full-stack Automation Engineer**. Hồ sơ của bạn đã cho thấy điểm mạnh nằm ở:

* Thiết kế pipeline dữ liệu.
* Xây dựng và đánh giá hệ thống AI một cách có phương pháp.
* Thiết kế cơ sở dữ liệu và quy trình xử lý.
* Trực quan hóa dữ liệu và báo cáo.
* Quản lý dự án và tài liệu hóa.

Vì vậy, trong toàn bộ bài test, hãy duy trì một thông điệp nhất quán:

> **"Tôi tiếp cận bài toán này như việc xây dựng một AI-driven data pipeline có khả năng kiểm soát chất lượng, theo dõi trạng thái, xử lý lỗi và đánh giá kết quả một cách có hệ thống."**

Đó là cách tận dụng tối đa nền tảng Python, SQL, Machine Learning, Graph Neural Networks, Data Visualization và kinh nghiệm ERP của bạn để tạo ra một bài làm có dấu ấn riêng, thay vì cố cạnh tranh với những ứng viên đã làm automation thuần túy nhiều năm.
