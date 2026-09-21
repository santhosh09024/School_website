# Apex International Academy - School Management Website & System

A complete, production-ready, modern, and responsive **School Management Website & Platform** built with Python, Flask, Flask-SQLAlchemy, Bootstrap 5, and JavaScript.

---

## 🌟 Features & Highlights

- **Public School Portal (30+ Pages)**: Home, About Us, Principal & Chairman Messages, Academics, Faculty Directory, Online Admissions, Student Life, News & Notices, Events Calendar, Photo & Video Gallery, Document Download Center, Examination Public Result Checker, Contact Us, FAQ, Privacy Policy, and Terms.
- **Role-Based Access Control (RBAC)**: Supports **Super Admin**, **Admin**, **Principal**, **Teacher**, **Student**, and **Parent** roles with distinct dashboard views and security scopes.
- **Student & Parent Management**: Full CRUD, admission number generation, photo upload, parent linkage, printable student identity card, CSV roster export.
- **Teacher Management**: Faculty directory, qualifications, subject/class assignments.
- **Daily Attendance System**: Teachers/Admins select class & date to mark Present, Absent, Late, or Leave. Generates real-time attendance percentage metrics and summary reports.
- **Examination & Marks Engine**: Exam terms setup, teacher marks entry, automatic total score, percentage, grade assignment (A+, A, B, C, D, F), and Pass/Fail evaluation.
- **Public Result Checker**: Online student lookup by Admission/Roll Number and Date of Birth with instant printable board marksheet.
- **Fee Management**: Custom fee categories, fee structures by class, payment recording, pending balance tracking, and printable fee receipt generation.
- **Timetable Management**: Define classes, sections, subjects, assign teachers, and view responsive timetable grids.
- **Content Management System (CMS)**: Post notices (with PDF upload), schedule events, create photo albums, and manage downloadable prospectus/syllabi documents.
- **RESTful APIs**: JSON endpoints (`/api/v1/stats`, `/api/v1/students`, `/api/v1/notices`, `/api/v1/events`, `/api/v1/results/<id>`) for dynamic frontend widgets.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Werkzeug.
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, FontAwesome 6, Chart.js.
- **Database**: SQLite (default zero-config local setup) / MySQL (Production compatible via SQLAlchemy `DATABASE_URL`).
- **Testing**: Python `unittest` test suite.

---

## 🔑 Demo Account Credentials

Use any of the following pre-seeded accounts to explore role-specific features:

| Role | Username | Password | Access Rights |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `superadmin` | `admin123` | Full System & Setting Control |
| **Admin** | `admin` | `admin123` | Student, Teacher, Fee & CMS Management |
| **Principal** | `principal` | `principal123` | Academic Oversight, Reports & Admissions |
| **Teacher** | `teacher_john` | `teacher123` | Attendance Marking & Marks Entry |
| **Parent** | `parent_robert` | `parent123` | Child Performance, Attendance & Fee Dues |
| **Student** | `student_alex` | `student123` | Personal Marks, Timetable & Attendance Log |

---

## 🚀 Quick Setup & Installation Guide

### Prerequisites
- Python 3.10 or higher installed.

### 1. Clone & Enter Project Directory
```bash
cd "d:\SANTHOSH\School website"
```

### 2. Create & Activate Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Default settings connect automatically to a local SQLite database at `instance/school.db`)*

To use **MySQL**, edit `.env`:
```env
DATABASE_URL=mysql+pymysql://username:password@localhost/school_db
```

### 5. Run the Application
```bash
python run.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

## 🧪 Running Automated Unit Tests

To run the full unit test suite:
```bash
python -m unittest discover tests
```

---

## 🌐 Production Deployment (Gunicorn & Nginx)

1. Set `FLASK_ENV=production` and update `SECRET_KEY` in `.env`.
2. Execute Gunicorn application server:
   ```bash
   gunicorn --bind 0.0.0.0:$PORT "run:app"
   ```
3. Configure Nginx as reverse proxy listening on port 80/443 forwarding to `http://127.0.0.1:5000`.

---

## 📄 License
© 2026 Apex International Academy. All Rights Reserved.


## ⚠️ GitHub Pages / GitHub Repository

This is a **Flask + Python + database application**. GitHub Pages cannot execute the Flask backend. GitHub is used to store the source code; deploy the application to a Python-capable host such as Render, Railway, or PythonAnywhere.

For Render, this repository includes `render.yaml`, `Procfile`, and `runtime.txt`. After connecting the repository, Render can build the app with `pip install -r requirements.txt` and start it with Gunicorn.

> Note: SQLite on many cloud hosts is ephemeral. For persistent production data, use a managed PostgreSQL/MySQL database and set `DATABASE_URL`.
