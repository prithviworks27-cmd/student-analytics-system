import customtkinter as ctk
from database import get_all_subjects, add_subject


class SubjectsScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._build_widgets()
        self._load_subjects()

    def _build_widgets(self):
        top_row = ctk.CTkFrame(self)
        top_row.pack(fill="x", padx=10, pady=10)

        self.name_entry = ctk.CTkEntry(top_row, width=250, placeholder_text="New subject name")
        self.name_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(top_row, text="Add Subject", command=self._on_add).pack(side="left")

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(anchor="w", padx=10)

        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Subjects")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _load_subjects(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        subjects = get_all_subjects()
        if not subjects:
            ctk.CTkLabel(self.list_frame, text="No subjects yet. Add one above.").pack(pady=10)
            return

        for subject in subjects:
            row = ctk.CTkFrame(self.list_frame)
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=subject["name"], anchor="w").pack(side="left", padx=5, fill="x", expand=True)

    def _on_add(self):
        name = self.name_entry.get().strip()
        if not name:
            self.error_label.configure(text="Please enter a subject name.")
            return

        try:
            add_subject(name)
        except Exception:
            self.error_label.configure(text="That subject already exists.")
            return

        self.error_label.configure(text="")
        self.name_entry.delete(0, "end")
        self._load_subjects()