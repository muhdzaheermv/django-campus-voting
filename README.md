# 🗳️ VoteSphere – Django-Based Campus E-Voting System

![Homepage](./vote/static/images/vp.png)

**VoteSphere** is a secure and dynamic **Campus E-Voting Platform** developed using **Django (Python)** along with **HTML, CSS, JavaScript, and Bootstrap**. It features multi-role authentication and functionality for **Admins**, **Election Officers**, **Presiding Officers**, and **Voters**, making it a full-stack, role-based voting solution for institutional needs.

## 🚀 Live Demo

👉 [Click here to view the live app](https://django-campus-voting.onrender.com/)

---

## 💠 Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
* **Libraries Used:**

  * `pandas`
  * `openpyxl`
  * `re`
  * `Django Authentication System`

---

## 👨‍💼 Admin Module Features

* Create & manage election campaigns
* Define positions (e.g., President, Secretary)
* Add/manage candidates
* Upload voter list via Excel
* Review and approve voter eligibility
* Assign Election & Presiding Officers
* Monitor **Live Election Results**
* Manage admin profile and settings

---

## 🧑‍💻 Election Officer Module

* Add/manage candidates
* Upload and manage voter list
* Edit voter records

---

## 🧑‍⚖️ Presiding Officer Module

* Review eligible voters
* Approve/disapprove voter status

---

## 🗳️ Voter Module

* Login with Student ID
* View elections & cast vote (one vote only)
* Auto logout after voting for vote integrity

---

## 🔐 Default Login Credentials

| Role              | Username / Email | Password    |
| ----------------- | ---------------- | ----------- |
| Admin             | `admin`          | `Pass@1234` |
| Election Officer  | `officer`        | `Pass@1234` |
| Presiding Officer | `officer`        | `Pass@1234` |

---

## 📸 Screenshot

![Homepage](./src/assets/images/homepage.png)

---

## 📁 Sample Code Snippet

```python
import pandas as pd
import re
import openpyxl
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
```

---

from `django.contrib.auth.hashers` import `make_password`, `check_password`

---

## 📚 Ideal Use Cases

🏫 College or university student elections
🏛️ Institutional digital voting systems
🧠 Django full-stack project learning
🔐 Role-based user authentication demo
📊 Secure admin dashboards for real-time data

---

## 🛋️ Contact Me

📧 **Email:** [muhdzaheermv@gmail.com](mailto:muhdzaheermv@gmail.com)
🌐 **Portfolio:** [https://portfolio-lilac-eight-60.vercel.app/](https://portfolio-lilac-eight-60.vercel.app/)
💼 **LinkedIn:** [https://www.linkedin.com/in/muhammed-zaheer-836132244/](https://www.linkedin.com/in/muhammed-zaheer-836132244/)

---

## ⭐ Like This Project?

If this project helped you, inspired your learning, or could be useful to your institution, please **give it a star ⭐ on GitHub!**
Your support keeps open-source projects like this alive 🙌

---
