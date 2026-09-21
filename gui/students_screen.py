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

    def _confirm_delete(self, student):
        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {student['name']} (Roll No: {student['roll_no']})?\n"
            "This will also delete their attendance and marks records."
        )
        if confirmed:
            delete_student(student["id"])
            self._load_students()

    def _open_add_form(self):
        self._open_student_form(title="Add Student", student=None)

    def _open_edit_form(self, student):
        self._open_student_form(title="Edit Student", student=student)

    def _open_student_form(self, title, student):
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("350x300")
        popup.grab_set()   # blocks interaction with the main window until this closes

        name_entry = ctk.CTkEntry(popup, placeholder_text="Full Name", width=250)
        name_entry.pack(pady=(20, 8))

        roll_entry = ctk.CTkEntry(popup, placeholder_text="Roll No.", width=250)
        roll_entry.pack(pady=8)

        class_entry = ctk.CTkEntry(popup, placeholder_text="Class (e.g. CSE-AIML)", width=250)
        class_entry.pack(pady=8)

        section_entry = ctk.CTkEntry(popup, placeholder_text="Section", width=250)
        section_entry.pack(pady=8)

        error_label = ctk.CTkLabel(popup, text="", text_color="red")
        error_label.pack(pady=(0, 5))

        if student:
            name_entry.insert(0, student["name"])
            roll_entry.insert(0, student["roll_no"])
            class_entry.insert(0, student["class_name"])
            section_entry.insert(0, student["section"])

        def on_save():
            name = name_entry.get().strip()
            roll_no = roll_entry.get().strip()
            class_name = class_entry.get().strip()
            section = section_entry.get().strip()

            if not (name and roll_no and class_name and section):
                error_label.configure(text="All fields are required.")
                return

            try:
                if student:
                    update_student(student["id"], name, roll_no, class_name, section)
                else:
                    add_student(name, roll_no, class_name, section)
            except Exception as e:
                error_label.configure(text="Roll number already exists.")
                return

            popup.destroy()
            self._load_students()

        ctk.CTkButton(popup, text="Save", command=on_save).pack(pady=15)