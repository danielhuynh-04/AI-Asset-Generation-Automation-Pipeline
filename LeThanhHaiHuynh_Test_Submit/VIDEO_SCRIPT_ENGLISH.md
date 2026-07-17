# 🎬 ENGLISH PRESENTATION SCRIPT - ATHENA STUDIO INTERN TEST
*Target time: Under 10 minutes. Goal: Confident, clear, and easy to pronounce.*

---

## 1. Introduction (0:00 - 1:00)
**[Show: Intro Slide / Portfolio]**
- Hello judges from Athena Studio. My name is Le Thanh Hai Huynh. I am applying for the Prompt Engineer and Automation Engineer Intern position.
- Today, I want to show you my project. I did not just write a simple script. I built a complete, production-ready Data Pipeline. I focused on making the system stable and secure.

---

## 2. Part A - Automation Architecture (1:00 - 4:00)
**[Show: Scroll down Github README.md to Architecture/BPMN Diagrams]**
- To generate assets automatically, my system has five main parts. In my Github README, I built both High-Level Architecture and BPMN workflow diagrams using Mermaid to clearly show how components interact.
- To save time, I used **ThreadPoolExecutor** to process many images at the same time.
- **Problem 1 (Database Lock):** When many threads write to SQLite, errors can happen. I fixed this by using the `check_same_thread=False` setting to make the database safe.
- **Problem 2 (API Error):** What if Google Gemini is down or out of quota? My code has an automatic fallback. It will switch to **ChatGPT (through Pollinations AI)** for free. This keeps the system running ninety-nine point nine percent (99.9%) of the time.
- **Idempotency (Safe to Restart):** The pipeline reads the Google Sheet and skips rows that are already marked as `DONE`. If the computer turns off, you can restart it safely without making duplicate images.

---

## 3. Part A - Demo & Security (4:00 - 6:00)
**[Show: Open VS Code Terminal, Type `python src/main.py`]**
- Now, let's watch the Demo. In the Google Sheet, I added the keyword `MOCK_TIMEOUT` to test errors.
- *(Point at Terminal)* As you can see, when a timeout happens, the system does not crash. It waits for 2 seconds, then 4 seconds. After 3 fails, it marks the job as FAILED and sends an alert.
- **Enterprise Security:** For sending Emails, I do not use risky SMTP App Passwords. Instead, I use **Google OAuth 2.0**. The admin just clicks "Allow" on the web browser once, and the script runs safely forever.

---

## 4. Part A - Daily Report (6:00 - 7:00)
**[Show: Type `python src/daily_report.py --run-now`, open HTML file]**
- Finally, I made a Daily Report module that runs automatically at 11 PM using **APScheduler**.
- *(Point at HTML Dashboard)* The report creates interactive Plotly charts, like Pie and Bar charts, to show the Success Rate and Execution Time. This HTML dashboard is sent straight to the admin's email.

---

## 5. Part B - Prompt Engineering Strategy (7:00 - 9:00)
**[Show: Open prompt_engineering_report.md]**
- Moving to Assignment 2. To generate sharp and accurate Bingo game assets, I analyzed five things: Art Style, Colors, Camera Angle, Lighting, and Details.
- My prompt structure is modular:
  `[Subject] + [Style: cel-shading] + [Lighting: inner glow] + [Camera: straight-on] + [Format: transparent background]`.
- *(Point at Iteration versions)* In version 1, colors were mixed up. I fixed this by using exact words like "Monochromatic Colorway". By version 3, the assets were ready to be used in the game engine.

---

## 6. Conclusion (9:00 - 10:00)
**[Show: Thank You Slide / Github Main Page]**
- I know this version has some limits. If we have a bigger budget, I suggest using Redis Queue instead of ThreadPool, and adding Cache to save API costs.
- In summary, this test shows my goal: to write clean, production-ready code that solves real business problems.
- Thank you for your time and for this great opportunity.
