# Exam Bill Management System
Welcome to the Exam Bill Management System project! This web application is designed to manage exam bills for the Jahangirnagar University Exam Office. Below are the key features and technologies used in this project:

## Features
- Account Management: Users can register for new accounts and log in using Django's built-in authentication system.

- Exam Committee Creation: The system allows the creation of exam committees consisting of a chairman and two tabulators.

- Course and Lab Exam Assignment: The chairman can assign courses and lab exams to faculty members.

- Bill Generation: The system generates bills for each faculty member based on their assigned courses and exams.

## Technologies Used
- HTML: For creating the structure of web pages.

- CSS: For styling the web pages and making them visually appealing.

- Bootstrap: For responsive design and pre-styled components.

- MySQL: As the database management system for storing data related to users, exam committees, course assignments, and bills.

- JavaScript: For adding interactivity and dynamic behavior to web pages.

- Django: The web framework used to develop the backend of the application, handling user authentication, data management, and business logic.

## Installation
Clone the repository to your local machine:

```git clone https://github.com/your-username/exam-bill-management-system.git```

Navigate to the project directory:

```cd exam-bill-management-system```

Install the required dependencies:

```pip install -r requirements.txt```

Set up the MySQL database and configure the database settings in the settings.py file.

Run migrations to create database tables:

```python manage.py makemigrations```
```python manage.py migrate ```
Start the development server:

```python manage.py runserver```
Access the application in your web browser at http://localhost:8000.
