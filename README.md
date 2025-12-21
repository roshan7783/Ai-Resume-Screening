# AI Resume Screening & Job Recommendation System

A web application that automatically analyzes resumes against a job description, extracts skills, calculates a match score, and provides a dashboard to view all analyzed resumes. Built with **Python Flask**, **MongoDB**, and modern frontend technologies.

---

## 🔹 Features

- Upload a resume (PDF) along with **Name, Email, College**.
- Analyze resume for skills and match score against a **Job Description**.
- Display skills as **badges** and match score with a **progress bar**.
- Save analyzed data to **MongoDB**.
- Dashboard to view all uploaded resumes with:
  - Name, Email, College
  - Skills (badges)
  - Match Score
  - Job Description
  - Date/Time of submission
- Fully responsive UI.
- Environment variables support for MongoDB URI (deployment-ready).

---

## 🔹 Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** MongoDB  
- **Libraries:** python-dotenv, pymongo, Flask  
- **Other:** Resume parsing & skill extraction modules (`resume_parser.py`, `matcher.py`, `skills.py`)

---

## 🔹 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-resume-screening.git
cd ai-resume-screening# Ai-Resume-Screening
