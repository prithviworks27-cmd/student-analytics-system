"""
login_screen.py
----------------
The first window the user sees. Checks credentials against the
'users' table, then hands off to the main Dashboard window.
"""

import customtkinter as ctk
from database import verify_login


class LoginScreen(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success  # callback -> called with the logged-in user row

        self.title("Student Analytics System - Login")
        self.geometry("400x350")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self._build_widgets()

    def _build_widgets(self):
        ctk.CTkLabel(
            self, text="Student Performance\nAnalytics System",
            font=ctk.CTkFont(size=20, weight="bold"), justify="center"
        ).pack(pady=(30, 10))

        ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.username_entry.pack(pady=8)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=8)
        # Pressing Enter in the password field also triggers login
        self.password_entry.bind("<Return>", lambda e: self._attempt_login())

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=(0, 5))

        ctk.CTkButton(
            self, text="Login", width=250, command=self._attempt_login
        ).pack(pady=10)

        ctk.CTkLabel(
            self, text="Default: admin / admin123",
            font=ctk.CTkFont(size=11), text_color="gray"
        ).pack(pady=(5, 0))

    def _attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.configure(text="Please enter both fields.")
            return

        user = verify_login(username, password)
        if user is None:
            self.error_label.configure(text="Invalid username or password.")
            return

        # Success — close login window and hand control to the dashboard
        self.destroy()
        self.on_login_success(user)
