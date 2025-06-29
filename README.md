# 🗳️ VoteSphere – Django-Based Campus E-Voting System

![Homepage](./src/assets/images/homepage.png)

**VoteSphere** is a secure, role-based **Campus E-Voting System** built with **Django (Python)** for the backend and **HTML, CSS, JS, Bootstrap** for the frontend. It features real-time voting, Excel voter upload, admin control, and vote integrity via automatic logout after submission.

## 🚀 Live Demo

👉 [Live App](https://django-campus-voting.onrender.com/)

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Libraries:** pandas, openpyxl, re, Django Auth, Excel handling

---

## 👨‍💼 Admin Module Features

- Create & manage election campaigns and positions
- Add/manage candidates
- Upload voter list via Excel
- View and approve eligible voters
- Appoint Election Officers and Presiding Officers
- View **Live Election Results**
- Manage admin profile and settings

---

## 🧑‍💻 Election Officer Module

- Add and manage candidate data
- Upload and edit voter lists
- Manage voter records

---

## 🧑‍⚖️ Presiding Officer Module

- Review eligible voters
- Approve or disapprove voter applications

---

## 🗳️ Voter Module

- Secure login with Student ID
- View elections and cast **one vote only**
- Automatic logout after voting

---

## 🔐 Default Login Credentials

| Role              | Username / Email | Password   |
|-------------------|------------------|------------|
| Admin             | `admin`          | `Pass@1234`|
| Election Officer  | `officer`        | `Pass@1234`|
| Presiding Officer | `officer`        | `Pass@1234`|

---

## ⚙️ Key Python Libraries & Snippets

```python
import pandas as pd
import re
import openpyxl
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
