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
git clone https://github.com/yourusername/scholaraid.git
cd scholaraid
2. 🌐 Create & Activate a Virtual Environment
👉 On Windows:
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
👉 On Linux/Mac:
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. 📦 Install Required Packages
bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt doesn't exist yet, create it with:

bash
Copy
Edit
pip freeze > requirements.txt
Main Dependencies:

shell
Copy
Edit
Django>=5.2.0
Pillow>=10.0  # For image uploads
Or install manually:

bash
Copy
Edit
pip install django pillow
4. ⚙️ Setup Database
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
Create an admin user (optional but recommended):

bash
Copy
Edit
python manage.py createsuperuser
5. 🚀 Run the Development Server
bash
Copy
Edit
python manage.py runserver
Then open your browser and go to:
http://127.0.0.1:8000

📁 Project Structure
bash
Copy
Edit
scholaraid/
├── users/              # Django app with models, views, templates
├── templates/          # All HTML templates
├── static/             # CSS, JS, icons, etc.
├── media/              # Uploaded images and files
├── db.sqlite3          # Default SQLite database
├── manage.py           # Django CLI tool
├── requirements.txt    # List of dependencies
└── README.md           # Project README
🧪 Tested On
Platform	Python Version	Django Version
Windows 10/11	3.12	5.2.3
Ubuntu 22.04	3.10	5.2.3

📝 Notes
Always activate the virtual environment before running the project.

Configure DEBUG=False and proper static/media file handling before deploying.

The database can be changed to PostgreSQL or MySQL for production.

Use Django admin panel to manage users and content as an administrator.

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙌 Contributing
Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

📬 Contact
For questions, feedback, or suggestions, contact:
📧 admin@scholaraid.org
🐙 github.com/yourusername
