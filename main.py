"""
main.py
-------
Entry point of the application. Run this file to start the app:

    python main.py

Flow: init the database -> show Login screen -> on success, show Dashboard.
"""
import sys
import os

if getattr(sys, 'frozen', False):
    # Running as a packaged app (PyInstaller) - stdout/stderr have nowhere
    # to go and can fill up and block. Redirect them to a log file instead.
    log_path = os.path.join(os.path.expanduser("~"), "student_analytics_log.txt")
    sys.stdout = open(log_path, "a")
    sys.stderr = sys.stdout

from database import init_db
from gui.login_screen import LoginScreen
from gui.dashboard import Dashboard


def launch_dashboard(user):
    """Called by LoginScreen once credentials are verified."""
    app = Dashboard(user)
    app.mainloop()


def main():
    init_db()  # creates school.db + tables on first run, no-op after that
    login = LoginScreen(on_login_success=launch_dashboard)
    login.mainloop()


if __name__ == "__main__":
    main()
