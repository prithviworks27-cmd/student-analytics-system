"""
dashboard.py
------------
The main window after login. For now this is a SHELL: a sidebar with
navigation buttons and an empty content area. In upcoming steps we'll
plug in the real screens (Students, Attendance, Marks, Analytics) by
swapping out what's shown in `self.content_area`.
"""

import customtkinter as ctk


class Dashboard(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        self.user = user  # the logged-in user's DB row (has .["username"], ["role"])

        self.title("Student Analytics System - Dashboard")
        self.geometry("950x600")

        self._build_layout()

    def _build_layout(self):
        # ---- Sidebar ----
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            sidebar, text=f"Welcome,\n{self.user['username']}",
            font=ctk.CTkFont(size=14, weight="bold"), justify="left"
        ).pack(pady=(20, 20), padx=15, anchor="w")

        nav_items = ["Students", "Attendance", "Marks", "Analytics"]
        for item in nav_items:
            ctk.CTkButton(
                sidebar, text=item, width=170,
                command=lambda i=item: self._show_placeholder(i)
            ).pack(pady=6, padx=15)

        ctk.CTkButton(
            sidebar, text="Logout", width=170, fg_color="#B22222",
            hover_color="#8B0000", command=self._logout
        ).pack(side="bottom", pady=20, padx=15)

        # ---- Content area (right side) ----
        self.content_area = ctk.CTkFrame(self)
        self.content_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self._show_placeholder("Home")

    def _show_placeholder(self, section_name):
        """Clears the content area and shows a placeholder label.
        Each of these will be replaced by a real screen in later steps."""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.content_area,
            text=f"{section_name} module\n(coming in the next build step)",
            font=ctk.CTkFont(size=18)
        ).pack(expand=True)

    def _logout(self):
        self.destroy()
        # Re-import here to avoid a circular import at module load time
        from gui.login_screen import LoginScreen
        from main import launch_dashboard
        LoginScreen(on_login_success=launch_dashboard).mainloop()
