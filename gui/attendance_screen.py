import customtkinter as ctk
from datetime import date
from database import get_all_subjects, get_attendance_for_date, mark_attendance


class AttendanceScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.subjects = get_all_subjects()
        self.status_buttons = {}   # maps student_id -> {"Present": button, "Absent": button}

        self._build_widgets()

    def _build_widgets(self):
        # --- Top row: date entry + subject dropdown ---
        top_row = ctk.CTkFrame(self)
        top_row.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(top_row, text="Date (YYYY-MM-DD):").pack(side="left", padx=(0, 5))
        self.date_entry = ctk.CTkEntry(top_row, width=120)
        self.date_entry.insert(0, str(date.today()))   # defaults to today
        self.date_entry.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(top_row, text="Subject:").pack(side="left", padx=(0, 5))
        subject_names = [s["name"] for s in self.subjects]
        self.subject_dropdown = ctk.CTkOptionMenu(top_row, values=subject_names)
        self.subject_dropdown.pack(side="left", padx=(0, 20))

        ctk.CTkButton(top_row, text="Load Students", command=self._load_students).pack(side="left")

        # --- Scrollable area where student rows will appear ---
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Students")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _load_students(self):
        # Clear out any rows from a previous load (e.g. switching subjects)
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.status_buttons = {}

        subject_name = self.subject_dropdown.get()
        subject_id = next(s["id"] for s in self.subjects if s["name"] == subject_name)
        selected_date = self.date_entry.get()

        students = get_attendance_for_date(subject_id, selected_date)

        for student in students:
            self._build_student_row(student, subject_id, selected_date)

    def _build_student_row(self, student, subject_id, selected_date):
        row = ctk.CTkFrame(self.list_frame)
        row.pack(fill="x", pady=4)

        label_text = f"{student['name']} ({student['roll_no']})"
        ctk.CTkLabel(row, text=label_text, width=250, anchor="w").pack(side="left", padx=5)

        present_btn = ctk.CTkButton(
            row, text="Present", width=90,
            fg_color="green" if student["status"] == "Present" else "gray",
            command=lambda: self._set_status(student["student_id"], subject_id, selected_date, "Present")
        )
        present_btn.pack(side="left", padx=5)

        absent_btn = ctk.CTkButton(
            row, text="Absent", width=90,
            fg_color="red" if student["status"] == "Absent" else "gray",
            command=lambda: self._set_status(student["student_id"], subject_id, selected_date, "Absent")
        )
        absent_btn.pack(side="left", padx=5)

        self.status_buttons[student["student_id"]] = {"Present": present_btn, "Absent": absent_btn}

    def _set_status(self, student_id, subject_id, selected_date, status):
        mark_attendance(student_id, subject_id, selected_date, status)

        present_btn = self.status_buttons[student_id]["Present"]
        absent_btn = self.status_buttons[student_id]["Absent"]
        present_btn.configure(fg_color="green" if status == "Present" else "gray")
        absent_btn.configure(fg_color="red" if status == "Absent" else "gray")