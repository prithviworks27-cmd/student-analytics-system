import customtkinter as ctk
from database import get_all_subjects, get_class_marks, add_marks


class MarksScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.subjects = get_all_subjects()
        self.mark_entries = {}   # maps student_id -> {"obtained": entry, "max": entry, "status": label}

        self._build_widgets()

    def _build_widgets(self):
        top_row = ctk.CTkFrame(self)
        top_row.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(top_row, text="Exam Type:").pack(side="left", padx=(0, 5))
        self.exam_entry = ctk.CTkEntry(top_row, width=140, placeholder_text="e.g. Mid-Term")
        self.exam_entry.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(top_row, text="Subject:").pack(side="left", padx=(0, 5))
        subject_names = [s["name"] for s in self.subjects]
        self.subject_dropdown = ctk.CTkOptionMenu(top_row, values=subject_names)
        self.subject_dropdown.pack(side="left", padx=(0, 20))

        ctk.CTkButton(top_row, text="Load Students", command=self._load_students).pack(side="left")

        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Students")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _load_students(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.mark_entries = {}

        subject_name = self.subject_dropdown.get()
        subject_id = next(s["id"] for s in self.subjects if s["name"] == subject_name)
        exam_type = self.exam_entry.get().strip()

        if not exam_type:
            ctk.CTkLabel(self.list_frame, text="Please enter an exam type first.", text_color="red").pack()
            return

        students = get_class_marks(subject_id, exam_type)

        for student in students:
            self._build_student_row(student, subject_id, exam_type)

    def _build_student_row(self, student, subject_id, exam_type):
        row = ctk.CTkFrame(self.list_frame)
        row.pack(fill="x", pady=4)

        label_text = f"{student['name']} ({student['roll_no']})"
        ctk.CTkLabel(row, text=label_text, width=220, anchor="w").pack(side="left", padx=5)

        obtained_entry = ctk.CTkEntry(row, width=70, placeholder_text="Marks")
        if student["marks_obtained"] is not None:
            obtained_entry.insert(0, str(student["marks_obtained"]))
        obtained_entry.pack(side="left", padx=5)

        ctk.CTkLabel(row, text="/").pack(side="left")

        max_entry = ctk.CTkEntry(row, width=70, placeholder_text="Max")
        max_entry.insert(0, str(student["max_marks"]) if student["max_marks"] is not None else "100")
        max_entry.pack(side="left", padx=5)

        status_label = ctk.CTkLabel(row, text="", width=100)
        status_label.pack(side="left", padx=5)

        save_btn = ctk.CTkButton(
            row, text="Save", width=70,
            command=lambda: self._save_marks(student["student_id"], subject_id, exam_type)
        )
        save_btn.pack(side="left", padx=5)

        self.mark_entries[student["student_id"]] = {
            "obtained": obtained_entry, "max": max_entry, "status": status_label
        }

    def _save_marks(self, student_id, subject_id, exam_type):
        entries = self.mark_entries[student_id]
        obtained_text = entries["obtained"].get().strip()
        max_text = entries["max"].get().strip()

        try:
            obtained = float(obtained_text)
            max_marks = float(max_text)
        except ValueError:
            entries["status"].configure(text="Enter numbers", text_color="red")
            return

        if obtained < 0 or max_marks <= 0 or obtained > max_marks:
            entries["status"].configure(text="Invalid range", text_color="red")
            return

        add_marks(student_id, subject_id, exam_type, obtained, max_marks)
        entries["status"].configure(text="Saved!", text_color="green")

    