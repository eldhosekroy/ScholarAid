# 🎓 ScholarAid – Empowering Education for All

![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue)
![Built with](https://img.shields.io/badge/Built%20With-Django%20%7C%20SQLite3-orange)

ScholarAid is a Django-based platform designed to support underprivileged students through a structured scholarship system. Students can apply for scholarships, attend exams, get evaluated, and receive aid, while sponsors can create and manage scholarship opportunities.

---

## ✨ Features

- 🧑‍🎓 Student registration and scholarship application
- 📝 Exam system linked to each scholarship
- 📈 Automatic scoring and result tracking
- 🏆 Sponsor dashboard to manage scholarships, view applicants, and approve awards
- 💬 Review and feedback system with admin and sponsor replies
- 🔐 Role-based access (admin, sponsor, student)
- 📬 Email/contact field for communication

---

## 🛠️ Setup Instructions

### 1. 🔁 Clone the Repository

```bash
git clone https://github.com/eldhosekroy/ScholarAid
cd scholaraid
```

### 2. 🌐 Create & Activate a Virtual Environment

👉 On Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

👉 On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 📦 Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. ⚙️ Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 🚀 Run the Development Server
```bash
python manage.py runserver
```
