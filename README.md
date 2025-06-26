# 🗳️ VoteSphere – Django-Based Campus E-Voting System

[![Stars](https://img.shields.io/github/stars/yourusername/votesphere?style=social)](https://github.com/yourusername/votesphere/stargazers)
[![Forks](https://img.shields.io/github/forks/yourusername/votesphere?style=social)](https://github.com/yourusername/votesphere/network/members)
![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![Django](https://img.shields.io/badge/Django-4.x-green.svg)
![License](https://img.shields.io/github/license/yourusername/votesphere)

A secure, full-stack **Django e-voting system** for campus elections. VoteSphere enables students to cast their votes online through a responsive interface powered by **Bootstrap**, **HTML**, **CSS**, and **JavaScript**, while the backend is handled by **Django** and essential **Python libraries**.

> 🎓 Ideal for final-year academic projects, demo apps, or learning Django full-stack development.

---

## 🔗 Live Demo & Video

* 🌐 **Hosted Demo:** [https://votesphere-demo.yourdomain.com](https://votesphere-demo.yourdomain.com)
* 🎮 **Demo Video:** [Watch on YouTube](https://www.youtube.com/watch?v=your-demo-video-link)

---

## 🚀 Key Features (Role-Based Access)

### 👨‍💼 Admin Module

1. Create/manage election campaigns
2. Create/manage election positions (President, Secretary, etc.)
3. Create/manage candidates
4. Upload voter list via Excel
5. View/approve eligible voters
6. Create/manage Election Officers & Presiding Officers
7. View live election results
8. Admin profile and settings

### 🧑‍💻 Election Officer Module

1. Create/manage candidates
2. Upload voter list
3. Edit voter data and manage voter records

### 🧑‍⚖️ Presiding Officer Module

1. Review eligible voters
2. Approve or disapprove voter eligibility

### 🗳️ Voter Module

1. Login with **Voter Student ID**
2. View election and cast vote (one vote only)
3. Automatic logout after voting

---

## 🔐 Default Login Credentials

| Role               | Username / Email       | Password    |
| ------------------ | ---------------------- | ----------- |
| Superuser (Django) | `admin@votesphere.com` | `123`       |
| Admin              | `admin`                | `Pass@1234` |
| Election Officer   | `officer`              | `Pass@1234` |
| Presiding Officer  | `officer`              | `Pass@1234` |

---

## 💻 Tech Stack

### Frontend:

* HTML, CSS, Bootstrap 5
* JavaScript

### Backend:

* Django (Python Web Framework)

### Python Libraries:

```python
import pandas as pd
import re
import openpyxl
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
```

---

## 📸 Screenshots

> *(Include images of the dashboard, voting page, login page, result view, etc.)*

---

## 📦 How to Run This Project Locally

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/votesphere.git
   cd votesphere
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser (Optional)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Visit Your App**

   ```
   http://127.0.0.1:8000/
   ```

---

## 📚 Ideal Use Cases

* 🎓 Final-year Computer Science or IT projects
* 🗳️ College and university student elections
* 👨‍💻 Full-stack Django learning projects
* 🔐 Secure voting system simulations

---

## 🤝 Contributing

We welcome contributions!
Fork the repo, create a branch, commit changes, and open a pull request.

---

## 🌟 Support This Project

If you find this project helpful:

* ⭐ Star this repository
* 📢 Share with friends and student communities
* 🧑‍💻 Use it in your final year project and give credit!

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 📧 Contact

**Created by:** \[Your Name]
📬 Email: [your.email@example.com](mailto:your.email@example.com)
🔗 GitHub: [@yourusername](https://github.com/yourusername)
🔗 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
