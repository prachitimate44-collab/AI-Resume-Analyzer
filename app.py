from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files.get("resume")

    if not file:
        return "No resume uploaded"


    # Read PDF
    pdf_reader = PyPDF2.PdfReader(file)

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() or ""


    resume_text = text.lower()


    # Get Job Description
    job = request.form.get("job")

    if job is None:
        job = ""

    job = job.lower()


    print("JOB TEXT:", job)


    skills = [
        "python",
        "ai",
        "sql",
        "flask",
        "machine learning",
        "java",
        "html",
        "css",
        "javascript"
    ]


    # Resume skills
    found_skills = []

    for skill in skills:
        if skill in resume_text:
            found_skills.append(skill)


    score = int((len(found_skills) / len(skills)) * 100)


    # Job Match
    matched = []

    for skill in skills:
        if skill in job:
            matched.append(skill)


    if len(skills) > 0:
        job_match = int((len(matched) / len(skills)) * 100)
    else:
        job_match = 0


    missing = []

    for skill in skills:
        if skill not in resume_text:
            missing.append(skill)


    suggestions = []

    if missing:
        suggestions.append("Add missing skills to your resume")


    return render_template(
        "result.html",
        score=score,
        job_match=job_match,
        skills=found_skills,
        missing=missing,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)