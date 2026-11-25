import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import markdown
import bleach

load_dotenv()
app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL", "https://api.deepseek.com")
)
MODEL = os.getenv("MODEL", "deepseek-chat")

ALLOWED_TAGS = set(bleach.sanitizer.ALLOWED_TAGS).union({
    "p", "h1", "h2", "h3", "h4", "ul", "ol", "li",
    "strong", "em", "blockquote", "pre", "code", "hr", "br"
})
ALLOWED_ATTRIBUTES = {"a": ["href", "title"]}


def render_markdown_safely(text):
    """Convert model Markdown to safe HTML for display."""
    html = markdown.markdown(text or "", extensions=["extra", "sane_lists"])
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols={"http", "https", "mailto"},
        strip=True
    )


def ask_deepseek(tasks, previous_plan=None):
    if not os.getenv("API_KEY"):
        raise ValueError("API_KEY is missing. Add your DeepSeek key to the .env file.")

    if previous_plan:
        system_prompt = (
            "You are a careful university study-planning assistant. "
            "Use the corrected task information as the source of truth. "
            "Compare it with the previous plan, explain what changed, and produce a revised plan. "
            "Do not claim that a task was changed unless the new input supports that."
        )
        user_prompt = f"""
The student has corrected their assignment information.

PREVIOUS PLAN:
{previous_plan}

UPDATED ASSIGNMENT INFORMATION (use this as the source of truth):
{tasks}

Please:
1. Re-rank all tasks using the updated information.
2. Create a revised, realistic study schedule.
3. Explain why each task has its priority.
4. Add a short section called "What changed after the correction".
5. State any assumptions and missing information.
6. Do not invent deadlines, available study hours, or personal commitments.

Use Markdown headings and concise bullet points.
"""
    else:
        system_prompt = (
            "You are a careful university study-planning assistant. "
            "Create realistic plans, explain recommendations, and clearly state uncertainty."
        )
        user_prompt = f"""
Create a study plan from the student's assignment information.

ASSIGNMENTS:
{tasks}

Please:
1. Rank tasks by urgency and importance.
2. Suggest a practical study schedule.
3. Explain briefly why each task has its priority.
4. Mention assumptions and missing information.
5. Do not invent deadlines, available study hours, or personal commitments.

Use Markdown headings and concise bullet points.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("The API returned an empty response.")
    return content


@app.route("/", methods=["GET", "POST"])
def index():
    tasks = ""
    result = None
    result_html = None
    error = None
    mode = None

    if request.method == "POST":
        tasks = request.form.get("tasks", "").strip()
        action = request.form.get("action", "generate")
        previous_plan = request.form.get("previous_plan", "").strip()

        if not tasks:
            error = "Please enter at least one assignment."
        elif action == "replan" and not previous_plan:
            error = "The previous plan is missing. Generate a plan before requesting a revision."
        else:
            try:
                result = ask_deepseek(
                    tasks=tasks,
                    previous_plan=previous_plan if action == "replan" else None
                )
                result_html = render_markdown_safely(result)
                mode = "revised" if action == "replan" else "generated"
            except Exception as exc:
                error = f"API request failed: {exc}"

    return render_template(
        "index.html",
        tasks=tasks,
        result=result,
        result_html=result_html,
        error=error,
        mode=mode
    )


if __name__ == "__main__":
    app.run(debug=True)
