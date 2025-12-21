from flask import Flask, request, jsonify, render_template
from datetime import datetime
from resume_parser import extract_text
from matcher import extract_skills, match_resume
from skills import SKILLS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# ---------------- LOAD ENV ----------------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("Error: MONGO_URI not found in environment variables!")

# ---------------- MONGO DB CONNECTION ----------------
client = MongoClient(MONGO_URI)
db = client["resume_analyzer_db"]
collection = db["analysis_results"]

# ---------------- FLASK APP ----------------
app = Flask(__name__)

# ---------------- HOME PAGE ----------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# ---------------- DASHBOARD PAGE ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ---------------- DASHBOARD DATA API ----------------
@app.route("/dashboard-data", methods=["GET"])
def dashboard_data():
    data = list(collection.find({}, {"_id": 0}).sort("created_at", -1))
    return jsonify(data)

# ---------------- ANALYZE RESUME ----------------
@app.route("/analyze", methods=["POST"])
def analyze():
    # Get user details
    name = request.form.get("name")
    email = request.form.get("email")
    college = request.form.get("college")
    job_desc = request.form.get("job", "")
    resume = request.files.get("resume")

    # Validation (mandatory fields)
    if not name or not email or not college or not resume:
        return jsonify({"error": "All fields are required"}), 400

    try:
        # Resume processing
        resume_text = extract_text(resume)
        skills_found = extract_skills(resume_text, SKILLS)
        match_score = match_resume(resume_text, job_desc)

        # Save data to MongoDB
        collection.insert_one({
            "name": name,
            "email": email,
            "college": college,
            "skills": skills_found,
            "match_score": match_score,
            "job_description": job_desc,
            "created_at": datetime.utcnow()
        })

        # Response to frontend
        return jsonify({
            "skills_found": skills_found,
            "match_score": match_score
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)