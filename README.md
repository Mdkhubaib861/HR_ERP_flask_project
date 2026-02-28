# HR_ERP - Human Resource ERP System

HR_ERP is a Flask-based Human Resource Management System designed to manage employee records efficiently.  
This web application allows administrators to perform CRUD operations and enables employees to view their details through a dashboard.

---

## 🚀 Features

- Employee Registration
- Employee Login
- Employee Dashboard
- Admin Dashboard
- Add Employee
- Edit Employee
- Delete Employee
- Search Employee
- View All Employees
- Upload Employee Photo
- MySQL Database Integration
- Responsive UI using Bootstrap 5

---

## 🛠️ Technologies Used

- Python
- Flask
- MySQL
- HTML5
- CSS3
- Bootstrap 5
- Jinja2

---

## 📂 Project Structure

HR_ERP/
│
├── static/
│   ├── assets/
│   ├── css/
│   ├── images/
│   ├── js/
│   └── vendors/
│
├── templates/
│   ├── add_employee.html
│   ├── admin_dashboard.html
│   ├── delete_employee.html
│   ├── edit_employee.html
│   ├── employee_dashboard.html
│   ├── employee_dashboard_login.html
│   ├── found_data.html
│   ├── index.html
│   ├── registration.html
│   ├── search_employee.html
│   ├── show_all.html
│   ├── update_record.html
│
├── main.py
├── requirements.txt
└── README.md

---

## ⚙️ Installation & Setup Guide

### 1️⃣ Clone the Repository

git clone https://github.com/Mdkhubai861/HR_ERP_flask_project.git

### 2️⃣ Navigate to Project Directory

cd HR_ERP

### 3️⃣ Create Virtual Environment (Recommended)

python -m venv venv

Activate (Windows):

venv\Scripts\activate

### 4️⃣ Install Dependencies

pip install -r requirements.txt

### 5️⃣ Configure MySQL Database

- Create database (example: hr_erp)
- Create table: emp_data
- Update database credentials inside main.py

### 6️⃣ Run the Application

python main.py

Open in browser:

http://127.0.0.1:5000

---

## 🗄️ Database Table Structure

Table Name: emp_data

Fields:

- eid (Primary Key)
- emp_name
- emp_email
- emp_mobile
- emp_gender
- emp_skill
- emp_dept
- emp_photo

---

## 👨‍💻 Author

Md Khubaib  
GitHub: https://github.com/Mdkhubai861

---

## 📜 License

This project is developed for learning and educational purposes.

---

⭐ If you like this project, give it a star!
