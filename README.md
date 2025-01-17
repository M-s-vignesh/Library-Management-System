# Library Management System 📚

A web-based application built with Python and Django to efficiently manage library operations such as book  member management, borrowing/returning books and adding books. This project provides a user-friendly interface for both administrators and users.

---

## Features ✨

- **User Management**: 
  - Librarin: Manage books, users, and issue/return records.
  - Users: Search books, view borrow history, and manage accounts.

- **Book Management**:
  - Add, update, and delete books from the catalog.
  - Search and filter books by title, author.

- **Borrow/Return System**:
  - Issue books to users and track return books.

- **Authentication**:
  - User registration, login, and logout.
  - Role-based access (Admin/Librarian/User).


---

## Tech Stack 🛠️

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default Django DB, configurable to PostgreSQL/MySQL)
- **Other Tools**: 
  - Bootstrap for UI styling

---

## Installation 🚀

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Apply database migrations:

bash
Copy
Edit
python manage.py migrate
Run the development server:

bash
Copy
Edit
python manage.py runserver
