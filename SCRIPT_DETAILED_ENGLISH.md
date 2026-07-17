# 🎬 ULTRA-DETAILED ENGLISH PRESENTATION SCRIPT
*Duration: Under 10 minutes | Read everything inside "..." out loud | Follow actions inside [...]*

---

## ⏱️ PART 1: INTRODUCTION (0:00 — 1:00)

### Actions:
- **[0:00]** Open Chrome browser, go to your Github Repo: `https://github.com/danielhuynh-04/AI-Asset-Generation-Automation-Pipeline`
- **[0:05]** Let the page load so the repo name and file tree are clearly visible.

### Speech:
> "Hello judges from Athena Studio.
> My name is Le Thanh Hai Huynh. I am applying for the **Prompt Engineer** and **Automation Engineer Intern** position.
>
> For this test, I did not just write a one-time script.
> I designed the entire system as a **Production-Ready Data Pipeline**. It has error handling, automatic recovery, and it can safely restart at any time without creating duplicate work.
>
> I will start by showing my System Architecture diagrams, and then run a live Demo."

---

## ⏱️ PART 2: EXPLAINING THE ARCHITECTURE DIAGRAM (1:00 — 3:00)

### Actions:
- **[1:00]** On the Github page, scroll down through `README.md` until you see the **first Mermaid diagram** (High-Level Architecture). Stop. Zoom in if needed (Ctrl + scroll up).
- **[1:10]** Slowly move your mouse over each box as you explain it.

### Speech:
> "This is the **Architecture Diagram** I coded using Mermaid syntax. Github renders it automatically.
>
> **(Move mouse to Google Sheets box)**
> The starting point is Google Sheets. When the admin enters data, the `sheets_reader` module scans and only picks rows that have NOT been processed yet. This is called **Idempotency** — no matter how many times you restart the system, it will never generate duplicate images. This saves 100% of wasted API costs.
>
> **(Move mouse to Validator box)**
> Next, data goes through the **Validator** module. It catches all bad data — empty descriptions, wrong formats like WEBP — before we waste money calling AI APIs.
>
> **(Move mouse to ThreadPoolExecutor box)**
> Valid data enters the **ThreadPoolExecutor** with 5 workers. Instead of processing image 1, then image 2, then image 3 one by one, the system generates **5 images at the same time**. This makes it 5 times faster."

---

## ⏱️ PART 3: FALLBACK MECHANISM & BPMN DIAGRAM (3:00 — 4:30)

### Actions:
- **[3:00]** Still on the README page. Move your mouse to the **"AI Generation Engine" subgraph** on the Architecture diagram.
- **[3:30]** Scroll down to the second diagram — **BPMN Sequence Diagram**. Stop in the middle of it.

### Speech:
> "**(Point at AI Generation Engine subgraph)**
> This is the AI core. By default, it calls **Google Gemini Imagen 3** to generate images. But free accounts only allow 10 images per day.
> So what happens when the quota runs out? My code handles this automatically: it **falls back** to **Pollinations Flux AI**, which is completely free, no API key needed. This keeps the system running at 99.9% uptime without any crashes.
>
> **(Point at Exponential Backoff box)**
> If the API has a network error, the system does NOT crash immediately. It waits 2 seconds, then 4 seconds, then 8 seconds — this is called **Exponential Backoff**. After 3 total failures, it marks the job as FAILED.
>
> **(Scroll to BPMN diagram)**
> Now, this is the **BPMN diagram** — a Business Process Model. You can see I split the system into 5 swimlanes: User, Orchestrator, AI Services, Storage, and Notifications.
> The key point here: the **Image Generation Loop** and the **Daily Reporting** run completely independently. The Report module is scheduled by **APScheduler** to run at exactly 11 PM every night, so it never slows down the main pipeline."

---

## ⏱️ PART 4: LIVE CODE DEMO (4:30 — 6:00)

### Actions:
- **[4:30]** Switch to **VS Code**. Open Terminal (Ctrl + `).
- **[4:35]** Type: `.\.venv\Scripts\python src/main.py` and press Enter.
- **[4:40]** Wait for log lines to appear. Watch for lines with `[SUCCESS]` and lines with `[RETRY]` or `[FAILED]`.
- **[5:10]** When you see a `MOCK_TIMEOUT` line, use your mouse to highlight (select) that line.

### Speech:
> "Now I will run the pipeline live. In my Google Sheet, I placed a test row with the keyword `MOCK_TIMEOUT` to simulate a network error.
>
> **(Point at SUCCESS lines)**
> As you can see, valid rows are processed successfully. Images are saved to Google Drive, and the system sends a Success notification through Slack and Email.
>
> **(Highlight the MOCK_TIMEOUT line)**
> And here, this row triggered a Timeout. But the system did NOT crash. It is retrying — attempt 1... attempt 2... attempt 3 — with increasing wait times. Finally, it logs the FAILED status into the SQLite Database and sends an Error alert email to the Admin immediately."

---

## ⏱️ PART 5: OAUTH 2.0 SECURITY (6:00 — 6:45)

### Actions:
- **[6:00]** Open `src/notifier.py` in VS Code. Scroll to the `_get_gmail_service()` function.
- **[6:15]** Highlight the lines containing `InstalledAppFlow` and `gmail_token.json`.

### Speech:
> "For sending emails, I completely removed the old SMTP App Password method because it stores passwords as plain text, which is very risky.
>
> **(Point at InstalledAppFlow line)**
> Instead, I integrated the **Gmail API using OAuth 2.0**. The first time the system runs, it opens a web browser and asks the Admin to click 'Allow'. After that, it creates a `gmail_token.json` file with a secure Refresh Token. From the second run onward, the system authenticates silently — no passwords needed.
>
> **(Point at gmail_token.json and token.json)**
> I also separated the tokens for Google Drive and Gmail. This follows the **Least Privilege** principle — each module only gets the exact permissions it needs, nothing more."

---

## ⏱️ PART 6: DAILY REPORT DASHBOARD (6:45 — 7:30)

### Actions:
- **[6:45]** Go back to VS Code Terminal. Type: `.\.venv\Scripts\python src/daily_report.py --run-now`
- **[7:00]** After the command finishes, open the HTML file from `report_sample/` folder by dragging it into Chrome.
- **[7:10]** Scroll through each chart on the HTML page (Pie Chart, Bar Chart, Scatter Plot).

### Speech:
> "This is the automated Daily Report Dashboard. I used the **Plotly** library to create interactive charts.
>
> **(Move mouse over the Pie Chart)**
> This pie chart shows the Success versus Failed ratio for the entire pipeline today.
>
> **(Move mouse over the Bar Chart)**
> This bar chart shows the number of jobs processed per day, so the Admin can track trends over time.
>
> **(Move mouse over the Scatter Plot)**
> And this scatter plot measures the Execution Time for each job. If any job is unusually slow, the Admin can spot it immediately.
>
> This entire HTML dashboard is automatically attached to an email and sent to the Admin at 11 PM every day."

---

## ⏱️ PART 7: PROMPT ENGINEERING — ASSIGNMENT 2 (7:30 — 9:00)

### Actions:
- **[7:30]** Open `prompt_engineering/prompt_engineering_report.md` in VS Code or on Github.
- **[7:45]** Scroll to the Analysis Matrix table (Art Style, Colors, Camera...).
- **[8:00]** Scroll to the comparison images showing V1 → V2 → V3 for each asset type (Characters, Balls, Buttons...).
- **[8:30]** Stop at the best-looking V3 Final image.

### Speech:
> "Moving to Assignment 2 — Prompt Engineering.
>
> **(Point at the Analysis Matrix table)**
> To generate accurate 2D Bingo game assets, I analyzed the original samples across 5 dimensions: Art Style, Hex Colors, Camera Angle, Lighting, and Detail Level. From this, I built a modular prompt structure.
>
> **(Scroll through V1 → V2 → V3 images)**
> In Version 1, the colors were mixed and inconsistent. I fixed this in V2 by adding the exact keyword 'Monochromatic Colorway'. By Version 3, the results are sharp and consistent — ready to be used directly in a Game Engine without editing.
>
> **(Stop at V3 image)**
> Every iteration is fully documented: the exact Prompt used, Problems found, How I fixed them, and a Quality Score from 1 to 5."

---

## ⏱️ PART 8: CONCLUSION & FUTURE IMPROVEMENTS (9:00 — 10:00)

### Actions:
- **[9:00]** Go back to the Github Repo page. Scroll down to the **Known Limitations & Future Work** table in README.
- **[9:30]** Scroll back up to the top of the page to end on the Repo title.

### Speech:
> "**(Point at the Limitations table)**
> I clearly understand the current limitations. SQLite is only suitable for single-user scenarios. The in-process queue cannot handle thousands of jobs.
>
> If given a production environment with budget, I propose two improvements:
> First, migrate the job queue to **Celery with Redis** for distributed processing.
> Second, implement **SHA-256 Hash Caching** — if the same prompt appears twice, the system skips it and reuses the previous result. This dramatically reduces API costs.
>
> **(Scroll back to the top)**
> Although this is a small-scale project, I hope it demonstrates my **System Mindset** — my ability to think about real-world problems like security, scalability, and reliability.
> I truly look forward to the opportunity to learn and grow at Athena Studio.
> Thank you very much for your time!"

---

## ✅ PRE-RECORDING CHECKLIST

| # | Item | Check |
|---|---|---|
| 1 | Github Repo page already open in Chrome | ☐ |
| 2 | VS Code open with Terminal (`.venv` activated) | ☐ |
| 3 | Google Sheet has sample data (including a `MOCK_TIMEOUT` row) | ☐ |
| 4 | Files `credentials.json`, `token.json`, `gmail_token.json` exist | ☐ |
| 5 | Folder `report_sample/` has at least 1 sample HTML file | ☐ |
| 6 | Microphone + Screen recorder (OBS Studio / Loom) ready | ☐ |
| 7 | Read through the script once before recording | ☐ |
