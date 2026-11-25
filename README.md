# StudyFlow AI Planner

A lightweight intelligent interactive system prototype for generating explainable study plans and allowing students to correct assignment information and request a revised plan.

## Project status

**Working prototype; initial generation and correction/replanning flow demonstrated.**

The report documents six screenshots captured from the running prototype. The screenshots should be uploaded into the `images/` folder using the filenames listed in the report. The repository currently contains the report and application source; screenshot binaries are not yet present.

This is a functional demonstration, not evidence of a formal user study or improved academic outcomes.

## Features implemented

- Enter assignment names, deadlines, estimated workloads and importance.
- Send the task description to DeepSeek through a Flask backend.
- Display a generated priority ranking, study schedule, rationale and assumptions.
- Edit the task description after reviewing the first response.
- Send corrected task information and the previous plan to DeepSeek.
- Display the revised plan and an explanation of what changed.
- Render the model's Markdown response as formatted HTML.

## Technology stack

- Python and Flask
- HTML and CSS
- DeepSeek API through the OpenAI-compatible Python SDK
- `python-dotenv` for local environment configuration
- `Markdown` and `bleach` for Markdown conversion and HTML sanitisation

## Project structure

```text
AI-Study-Planner/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── images/                         # Upload the six evidence screenshots here
└── docs/
    └── A2_Project_Report.md
```

## Run locally

1. Install Python 3.10 or later.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env`.
4. Add your DeepSeek API key to `.env`:

   ```env
   API_KEY=your_deepseek_api_key
   BASE_URL=https://api.deepseek.com
   MODEL=deepseek-chat
   ```

5. Start the application:

   ```bash
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

**Security:** Never commit `.env` or any API key. The `.env` file is listed in `.gitignore`. Do not put the key in HTML or screenshots.

## How to test the correction interaction

1. Enter two assignments:
   - Research Essay — deadline: 28 November 2026 — estimated workload: 6 hours — importance: high
   - Group Project — deadline: 2 December 2026 — estimated workload: 4 hours — importance: medium
2. Select **Generate my study plan**.
3. Review the ranking, schedule, priority rationale and assumptions.
4. In **Correct your information and replan**, change the Group Project deadline to 26 November 2026.
5. Select **Save correction and regenerate plan**.
6. Check that the revised response considers the earlier deadline and explains the change.

## Architecture

The browser sends task information to Flask. Flask constructs a prompt and calls the DeepSeek API. The response is returned to the browser. For replanning, Flask sends both the corrected task description and the previous plan to the model.

See the system diagram and interaction scenarios in [the A2 Project Report](docs/A2_Project_Report.md).

## Development record

- Created the initial HTML/CSS assignment input page.
- Added a Flask route to receive assignment text and call the DeepSeek API.
- Confirmed that the API generated a task ranking, schedule, priority rationale and assumptions for a two-task example.
- Added a correction form that allows assignment information to be edited after the first response.
- Added a replanning request that sends corrected task information and the previous response to DeepSeek.
- Demonstrated a deadline correction from 2 December to 26 November 2026; the revised response ranked the Group Project first and described the change.
- Added Markdown rendering and sanitisation for the model response.

## AI assistance

AI assistance was used to help draft and revise parts of the Python, HTML/CSS, report and documentation. The project author ran the application, configured the API key locally, exercised the initial and correction interactions, and supplied the screenshots included as development evidence. The code and generated recommendations should be reviewed by the project author.

## Limitations and future work

- Tasks are not saved in a database or retained between separate sessions.
- The prototype does not connect to a calendar or check real availability.
- The model may misunderstand ambiguous task descriptions or produce an impractical schedule.
- The correction flow relies on the user to notice and edit inaccurate information.
- No formal usability study or learning-outcome evaluation has been conducted.

Potential future work includes structured task fields, validation of extracted deadlines, persistent storage, calendar integration and evaluation with students. These are not implemented features.
