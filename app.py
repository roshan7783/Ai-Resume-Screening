from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
from resume_parser import extract_text
from matcher import extract_skills, match_resume
from skills import SKILLS
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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
users_collection = db["users"]

# ---------------- FLASK APP ----------------
app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.email = user_data["email"]
        self.password = user_data["password"]

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

# ---------------- HOME PAGE ----------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# ---------------- LOGIN PAGE ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_data = users_collection.find_one({"email": email})

        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return "Invalid email or password"
    return render_template("login.html")

# ---------------- REGISTER PAGE ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        # For simplicity, the first user to register is the admin
        if users_collection.count_documents({}) == 0:
            users_collection.insert_one({"email": email, "password": hashed_password, "is_admin": True})
        else:
            users_collection.insert_one({"email": email, "password": hashed_password, "is_admin": False})

        return redirect(url_for("login"))
    return render_template("register.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ---------------- DASHBOARD PAGE ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# ---------------- DASHBOARD DATA API ----------------
@app.route("/dashboard-data", methods=["GET"])
@login_required
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