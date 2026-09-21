import customtkinter as ctk
from tkinter import messagebox
from database import get_all_students, search_students, add_student, update_student, delete_student


class StudentsScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._build_widgets()
        self._load_students()

    def _build_widgets(self):
        top_row = ctk.CTkFrame(self)
        top_row.pack(fill="x", padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(top_row, width=250, placeholder_text="Search by name or roll no.")
        self.search_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(top_row, text="Search", width=90, command=self._on_search).pack(side="left", padx=(0, 20))
        ctk.CTkButton(top_row, text="+ Add Student", width=130, command=self._open_add_form).pack(side="left")

        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Students")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _load_students(self, keyword=None):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        students = search_students(keyword) if keyword else get_all_students()

        if not students:
            ctk.CTkLabel(self.list_frame, text="No students found.").pack(pady=10)
            return

        for student in students:
            self._build_student_row(student)

    def _on_search(self):
        keyword = self.search_entry.get().strip()
        self._load_students(keyword if keyword else None)

    def _build_student_row(self, student):
        row = ctk.CTkFrame(self.list_frame)
        row.pack(fill="x", pady=4)

        info_text = f"{student['name']}  |  Roll: {student['roll_no']}  |  {student['class_name']} - {student['section']}"
        ctk.CTkLabel(row, text=info_text, anchor="w").pack(side="left", padx=5, fill="x", expand=True)

        ctk.CTkButton(
            row, text="Edit", width=70,
            command=lambda s=student: self._open_edit_form(s)
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            row, text="Delete", width=70, fg_color="#B22222", hover_color="#8B0000",
            command=lambda s=student: self._confirm_delete(s)
        ).pack(side="left", padx=5)