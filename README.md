# Student Performance Analytics & Attendance Management System

## What's built so far (Week 1-3 of the roadmap)
- `database.py` — SQLite schema: users, students, subjects, attendance, marks
- `gui/login_screen.py` — login window, checks credentials against the DB
- `gui/dashboard.py` — post-login shell with sidebar nav (Students / Attendance / Marks / Analytics placeholders)
- `main.py` — entry point wiring it all together

## How to run it on your own PC
1. Install Python 3.10+ if you don't have it.
2. Open a terminal in this folder and install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python main.py
   ```
4. Log in with the default seeded account:
   - Username: `admin`
   - Password: `admin123`

The first run creates `school.db` automatically in this folder — that's your entire database, no server needed.

## What's next
- Student CRUD screen (add/edit/delete/search students) — replaces the "Students" placeholder
- Subject management
- Attendance marking screen
- Marks entry screen
- Analytics dashboard + the ML "At-Risk" classifier
- PDF/Excel report export

We're building these one at a time, the same way we just did the login + dashboard shell.
