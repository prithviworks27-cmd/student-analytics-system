import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import get_all_subjects, get_attendance_trend, get_grade_distribution


class AnalyticsScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.subjects = get_all_subjects()
        self._build_widgets()

    def _build_widgets(self):
        top_row = ctk.CTkFrame(self)
        top_row.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(top_row, text="Subject:").pack(side="left", padx=(0, 5))
        subject_names = [s["name"] for s in self.subjects]
        self.subject_dropdown = ctk.CTkOptionMenu(top_row, values=subject_names)
        self.subject_dropdown.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(top_row, text="Exam Type:").pack(side="left", padx=(0, 5))
        self.exam_entry = ctk.CTkEntry(top_row, width=140, placeholder_text="e.g. Mid-Term")
        self.exam_entry.pack(side="left", padx=(0, 20))

        ctk.CTkButton(top_row, text="Load Analytics", command=self._load_analytics).pack(side="left")

        charts_row = ctk.CTkFrame(self)
        charts_row.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Left: attendance trend line chart
        self.trend_fig = Figure(figsize=(4.5, 3.5), dpi=100)
        self.trend_ax = self.trend_fig.add_subplot(111)
        self.trend_canvas = FigureCanvasTkAgg(self.trend_fig, master=charts_row)
        self.trend_canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)

        # Right: grade distribution bar chart
        self.grade_fig = Figure(figsize=(4.5, 3.5), dpi=100)
        self.grade_ax = self.grade_fig.add_subplot(111)
        self.grade_canvas = FigureCanvasTkAgg(self.grade_fig, master=charts_row)
        self.grade_canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)

    def _load_analytics(self):
        subject_name = self.subject_dropdown.get()
        subject_id = next(s["id"] for s in self.subjects if s["name"] == subject_name)
        exam_type = self.exam_entry.get().strip()

        # --- Attendance trend (line chart) ---
        trend_data = get_attendance_trend(subject_id)
        self.trend_ax.clear()
        if trend_data:
            dates = [row[0] for row in trend_data]
            percentages = [row[1] for row in trend_data]
            self.trend_ax.plot(dates, percentages, marker="o", color="#1F3864")
            self.trend_ax.set_title("Attendance Trend")
            self.trend_ax.set_ylabel("% Present")
            self.trend_ax.tick_params(axis="x", rotation=45)
        else:
            self.trend_ax.set_title("No attendance data yet")
        self.trend_fig.tight_layout()
        self.trend_canvas.draw()

        # --- Grade distribution (bar chart) ---
        self.grade_ax.clear()
        if exam_type:
            buckets = get_grade_distribution(subject_id, exam_type)
            self.grade_ax.bar(buckets.keys(), buckets.values(), color="#943634")
            self.grade_ax.set_title(f"Grade Distribution - {exam_type}")
            self.grade_ax.set_ylabel("Number of Students")
            self.grade_ax.tick_params(axis="x", rotation=30)
        else:
            self.grade_ax.set_title("Enter an exam type")
        self.grade_fig.tight_layout()
        self.grade_canvas.draw()