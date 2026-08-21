# 💰 Expense Manager

A full-stack Expense Manager application built with **Python, FastAPI, SQLAlchemy, SQLite, HTML, CSS and JavaScript**.

The application allows users to create an account, securely log in using JWT authentication, and manage their personal expenses through a simple web dashboard.

---

## 🚀 Features

### Authentication

- User registration
- User login
- JWT-based authentication
- Secure password hashing using Argon2
- Protected API endpoints
- Logout functionality

### Expense Management

- Add new expenses
- View personal expenses
- Search expenses
- Update expenses
- Delete expenses
- User-specific expense data

### Backend

- RESTful API using FastAPI
- SQLAlchemy ORM
- SQLite database
- Pydantic schemas
- JWT authentication
- CORS configuration
- Swagger API documentation

### Frontend

- Registration page
- Login page
- Dashboard
- Add expense form
- Edit expense
- Delete expense
- Expense listing
- JWT token handling

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Python-Jose
- Argon2

### Frontend

- HTML5
- CSS3
- JavaScript

### Development Tools

- VS Code
- Git
- GitHub
- Swagger / OpenAPI

---

## 📁 Project Structure

```text
Expense_manager/
│
├── app/
│   │
│   ├── core/
│   │   ├── db.py
│   │   ├── security.py
│   │   └── jwt_helper.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── expense.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── expense.py
│   │
│   ├── schemas/
│   │   ├── api_response.py
│   │   ├── user.py
│   │   └── expenses.py
│   │
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   └── dashboard.html
│
├── test/
│
├── .gitignore
├── requirements.txt
└── README.md