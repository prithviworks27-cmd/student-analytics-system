"""
database.py
------------
Handles all SQLite database setup and connections for the
Student Performance Analytics & Attendance Management System.

Design note: we use a single file-based SQLite database (school.db).
No server, no internet needed — the whole app runs offline.
"""

import sqlite3
import os
import hashlib

DB_NAME = os.path.join(os.path.dirname(__file__), "school.db")


def get_connection():
    """Returns a new connection to the SQLite database.
    We enable foreign_keys so that deleting a student also cleans up
    their attendance/marks rows (see ON DELETE CASCADE below).
    """
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row  # lets us access columns by name, e.g. row["name"]
    return conn


def hash_password(password: str) -> str:
    """We never store plain-text passwords, even in a college mini project.
    SHA-256 is enough for this scope (not a production auth system)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    """Creates all tables if they don't already exist, and seeds a
    default admin user so you can log in on first run."""
    conn = get_connection()
    cur = conn.cursor()

    # --- Users table (login) ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'mentor'   -- 'admin' or 'mentor'
        )
    """)


    # --- Students table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL
        )
    """)

    # --- Subjects table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # --- Attendance table ---
    # status: 'Present' or 'Absent'
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            date TEXT NOT NULL,             -- stored as 'YYYY-MM-DD'
            status TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
            UNIQUE(student_id, subject_id, date)   -- prevents double-marking same day
        )
    """)

    # --- Marks table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            exam_type TEXT NOT NULL,         -- e.g. 'Mid-Term', 'Final'
            marks_obtained REAL NOT NULL,
            max_marks REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
            UNIQUE(student_id, subject_id, exam_type)
        )
    """)

    conn.commit()

    # --- Seed a default admin login if no users exist yet ---
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("admin", hash_password("admin123"), "admin"),
        )
        conn.commit()
        print("Default login created -> username: admin | password: admin123")

    conn.close()

def add_student(name, roll_no, class_name, section):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, roll_no, class_name, section) VALUES (?, ?, ?, ?)",
        (name, roll_no, class_name, section)
    )
    conn.commit()
    conn.close()

def get_all_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_students(keyword):
    conn = get_connection()
    cur = conn.cursor()
    like_pattern = f"%{keyword}%"
    cur.execute(
        "SELECT * FROM students WHERE name LIKE ? OR roll_no LIKE ? ORDER BY name",
        (like_pattern, like_pattern)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def update_student(student_id, name, roll_no, class_name, section):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name = ?, roll_no = ?, class_name = ?, section = ? WHERE id = ?",
        (name, roll_no, class_name, section, student_id)
    )
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

def add_subject(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_all_subjects():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM subjects ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows

def mark_attendance(student_id, subject_id, date, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO attendance (student_id, subject_id, date, status)
           VALUES (?, ?, ?, ?)
           ON CONFLICT(student_id, subject_id, date)
           DO UPDATE SET status = excluded.status""",
        (student_id, subject_id, date, status)
    )
    conn.commit()
    conn.close()

def get_attendance_for_date(subject_id, date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT students.id AS student_id, students.name, students.roll_no,
                  attendance.status
           FROM students
           LEFT JOIN attendance
             ON students.id = attendance.student_id
             AND attendance.subject_id = ?
             AND attendance.date = ?
           ORDER BY students.name""",
        (subject_id, date)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def get_attendance_percentage(student_id, subject_id=None):
    conn = get_connection()
    cur = conn.cursor()
    if subject_id:
        cur.execute(
            """SELECT
                   COUNT(*) AS total,
                   SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present_count
               FROM attendance
               WHERE student_id = ? AND subject_id = ?""",
            (student_id, subject_id)
        )
    else:
        cur.execute(
            """SELECT
                   COUNT(*) AS total,
                   SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present_count
               FROM attendance
               WHERE student_id = ?""",
            (student_id,)
        )
    row = cur.fetchone()
    conn.close()

    total = row["total"]
    present = row["present_count"] or 0
    if total == 0:
        return 0.0
    return round((present / total) * 100, 2)

def add_marks(student_id, subject_id, exam_type, marks_obtained, max_marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO marks (student_id, subject_id, exam_type, marks_obtained, max_marks)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(student_id, subject_id, exam_type)
           DO UPDATE SET marks_obtained = excluded.marks_obtained,
                         max_marks = excluded.max_marks""",
        (student_id, subject_id, exam_type, marks_obtained, max_marks)
    )
    conn.commit()
    conn.close()

def get_marks_for_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT subjects.name AS subject_name, marks.exam_type,
                  marks.marks_obtained, marks.max_marks
           FROM marks
           JOIN subjects ON marks.subject_id = subjects.id
           WHERE marks.student_id = ?
           ORDER BY subjects.name""",
        (student_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows
def get_class_marks(subject_id, exam_type):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT students.id AS student_id, students.name, students.roll_no,
                  marks.marks_obtained, marks.max_marks
           FROM students
           LEFT JOIN marks
             ON students.id = marks.student_id
             AND marks.subject_id = ?
             AND marks.exam_type = ?
           ORDER BY students.name""",
        (subject_id, exam_type)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def get_overall_percentage(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT SUM(marks_obtained) AS total_obtained, SUM(max_marks) AS total_max
           FROM marks
           WHERE student_id = ?""",
        (student_id,)
    )
    row = cur.fetchone()
    conn.close()

    total_obtained = row["total_obtained"] or 0
    total_max = row["total_max"] or 0
    if total_max == 0:
        return 0.0
    return round((total_obtained / total_max) * 100, 2)

def get_attendance_trend(subject_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT date,
                  COUNT(*) AS total,
                  SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present_count
           FROM attendance
           WHERE subject_id = ?
           GROUP BY date
           ORDER BY date""",
        (subject_id,)
    )
    rows = cur.fetchall()
    conn.close()

    trend = []
    for row in rows:
        pct = round((row["present_count"] / row["total"]) * 100, 2) if row["total"] else 0
        trend.append((row["date"], pct))
    return trend


def get_grade_distribution(subject_id, exam_type):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT marks_obtained, max_marks FROM marks
           WHERE subject_id = ? AND exam_type = ?""",
        (subject_id, exam_type)
    )
    rows = cur.fetchall()
    conn.close()

    buckets = {"0-40": 0, "40-60": 0, "60-75": 0, "75-90": 0, "90-100": 0}
    for row in rows:
        pct = (row["marks_obtained"] / row["max_marks"]) * 100
        if pct < 40:
            buckets["0-40"] += 1
        elif pct < 60:
            buckets["40-60"] += 1
        elif pct < 75:
            buckets["60-75"] += 1
        elif pct < 90:
            buckets["75-90"] += 1
        else:
            buckets["90-100"] += 1
    return buckets

def verify_login(username: str, password: str):
    """Returns the user row if credentials are correct, else None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    if user and user["password_hash"] == hash_password(password):
        return user
    return None


if __name__ == "__main__":
    # Running this file directly (python database.py) sets up the DB.
    init_db()
    print(f"Database ready at: {DB_NAME}")
