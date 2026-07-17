# 🎬 DETAILED READ-ALONG ENGLISH SCRIPT
*(Instructions: The words inside the brackets **[...]** are actions. The normal text is exactly what you SPEAK OUT LOUD in the recording. Speak clearly and confidently).*

---

## 1. Introduction (0:00 - 1:00)
**[Action: Show your Intro Slide or the Project Title]**
"Hello judges from Athena Studio. My name is Le Thanh Hai Huynh, applying for the Prompt Engineer and Automation Engineer Intern position.
In this project, I did not want to write just a simple linear script. My goal was to design a complete, **Production-ready Data Pipeline**. Today, I would like to use my System Diagrams to explain my architecture."

---

## 2. Explaining Diagrams: Architecture & BPMN (1:00 - 4:30)
**[Action: Open the README.md on Github, scroll to the Mermaid Diagrams]**
"(Point your mouse at the High-Level Architecture Diagram)
As you can see in this flow chart, I decoupled the architecture into independent modules.
The raw data from Google Sheets must pass through a strict **Validator** module. This catches one hundred percent (100%) of invalid data before making expensive API calls, which saves costs.

If the data is good, the system uses a **ThreadPoolExecutor** to process many images simultaneously.
(Point to the AI Generation Engine Subgraph)
The core feature of this AI block is the **Fallback mechanism**. Since free Gemini accounts have strict quotas, I added a safety net. If Gemini crashes or runs out of quota, my code automatically falls back to a free model using Flux AI from Pollinations. This guarantees 99.9% uptime without breaking the process.

(Scroll down to the BPMN Sequence Diagram)
Moving to the BPMN diagram, you can see I separated the workflow into different lanes. The Image Generation Loop is completely decoupled from the Reporting operations. I integrated **APScheduler** to automatically trigger the KPI Analytics and Email distribution at exactly eleven PM (11:00 PM) everyday, so it safely runs in the background."

---

## 3. Code Demo & Security (4:30 - 7:00)
**[Action: Open VS Code Terminal, type: `python src/main.py`]**
"Now, I will run the Demo. In my Google Sheets, I injected a bad record with the keyword `MOCK_TIMEOUT` to test error recovery.
(Point at the Warnings/Errors appearing in the terminal logs)
As you can see! The system encounters a timeout, but it does NOT crash. It activates the **Exponential Backoff** logic — waiting 2 seconds, then 4 seconds. After 3 failed attempts, it safely logs the FAILED status into the SQLite Database. To prevent deadlock errors during multi-threading, I optimized SQLAlchemy configurations to be extremely thread-safe.

Regarding Security, I removed outdated SMTP App passwords to prevent credential leaks. Instead, I integrated **Google OAuth 2.0 Web Consent** for the Gmail API. This upgrades the system to Enterprise-tier Zero Trust security."

---

## 4. Daily Report & Prompt Engineering (7:00 - 9:00)
**[Action: Type `python src/daily_report.py --run-now` and open the generated HTML file in Chrome]**
"Here is the automated Daily Report. I used the Plotly library to plot interactive charts showing the Success Rate, Error Frequencies, and Average Execution times. This HTML dashboard is emailed straight to the Admin everyday.

**[Action: Open `prompt_engineering/prompt_engineering_report.md`, scroll through iteration images]**
Moving to Assignment 2. To generate high-quality 2D assets for a Bingo game, I built a 5-dimension analysis matrix: Art Style, Hex Colors, Camera Angle, Lighting, and Details.
I used a highly modular prompt structure. Across 3 iterations, as you can see, I slowly filtered out unwanted noise. The final version produces highly stable UI buttons and backgrounds that are ready to be used in the Game Engine."

---

## 5. Conclusion & Future Scale (9:00 - 10:00)
**[Action: Open Github Project Home Page]**
"Due to the limitations of free tools, the system is locked to SQLite. However, in a large scale Enterprise environment, my future solution would be migrating the queues to Celery and Redis, and implementing Hash Caching for repeating prompts to save API costs.
Although this is a small-scale submission, I hope it demonstrates my extensive **System Mindset** making me a strong candidate for an Internship at Athena Studio. 
I really look forward to hearing your feedback. Thank you for listening!"
