import tkinter as tk
from datetime import datetime
from tkinter import ttk

from calendar_manager import CalendarManager
from reminder_manager import ReminderManager

WEEKDAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


class CalendarReminderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monthly Calendar Reminder App")
        self.configure(background="#eef2f3")

        self.calendar_manager = CalendarManager()
        self.reminder_manager = ReminderManager()
        self.current_date = datetime.now()

        self.year_var = tk.IntVar(value=self.current_date.year)
        self.month_var = tk.IntVar(value=self.current_date.month)
        self.month_name_var = tk.StringVar(value=MONTH_NAMES[self.current_date.month - 1])
        self.view_mode = tk.StringVar(value="month")

        self.create_widgets()
        self.refresh_calendar()
        self.refresh_reminder_list()

    def create_widgets(self):
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground="#1a4d7a", background="#eef2f3")
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 11), foreground="#52608a", background="#eef2f3")
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#0f3c5b", background="#eef2f3")
        self.style.configure("DayHeader.TLabel", font=("Segoe UI", 10, "bold"), foreground="#2b547e", background="#dfe7f2")
        self.style.configure("DayCell.TLabel", font=("Segoe UI", 10), foreground="#1f3b5a", background="#ffffff")
        self.style.configure("Card.TFrame", background="#ffffff")
        self.style.configure("Control.TFrame", background="#eef2f3")
        self.style.configure("Reminder.TLabelframe", background="#ffffff")
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#3f6cb9")
        self.style.map(
            "Primary.TButton",
            background=[("active", "#2f5bad"), ("!disabled", "#3f6cb9")],
            foreground=[("!disabled", "#ffffff")],
        )

        title_label = ttk.Label(self, text="Monthly Calendar Reminder App", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(16, 2), padx=16, sticky="w")


        control_frame = ttk.Frame(self, style="Control.TFrame", padding=(14, 14))
        control_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=16, pady=(10, 0))
        control_frame.columnconfigure(7, weight=1)

        ttk.Label(control_frame, text="Year:", background="#eef2f3").grid(row=0, column=0, sticky="w")
        self.year_spinbox = ttk.Spinbox(
            control_frame,
            from_=1900,
            to=2100,
            textvariable=self.year_var,
            width=6,
            command=self.refresh_calendar,
        )
        self.year_spinbox.grid(row=0, column=1, padx=(6, 20), sticky="w")

        ttk.Label(control_frame, text="Month:", background="#eef2f3").grid(row=0, column=2, sticky="w")
        self.month_combobox = ttk.Combobox(
            control_frame,
            values=MONTH_NAMES,
            textvariable=self.month_name_var,
            state="readonly",
            width=14,
        )
        self.month_combobox.grid(row=0, column=3, padx=(6, 20), sticky="w")
        self.month_combobox.bind("<<ComboboxSelected>>", self.on_month_selected)

        ttk.Radiobutton(
            control_frame,
            text="Month view",
            value="month",
            variable=self.view_mode,
            command=self.refresh_calendar,
        ).grid(row=0, column=4, padx=8)
        ttk.Radiobutton(
            control_frame,
            text="Year view",
            value="year",
            variable=self.view_mode,
            command=self.refresh_calendar,
        ).grid(row=0, column=5, padx=8)

        show_button = ttk.Button(control_frame, text="Refresh", style="Primary.TButton", command=self.refresh_calendar)
        show_button.grid(row=0, column=6, padx=4, sticky="e")

        self.header_label = ttk.Label(self, text="", style="Header.TLabel")
        self.header_label.grid(row=3, column=0, columnspan=2, padx=16, pady=(14, 6), sticky="w")

        self.calendar_frame = ttk.Frame(self, style="Card.TFrame", padding=14)
        self.calendar_frame.grid(row=4, column=0, sticky="nsew", padx=(16, 8), pady=(0, 16))
        self.calendar_frame.columnconfigure(0, weight=1)
        self.calendar_frame.rowconfigure(0, weight=1)

        self.calendar_canvas = tk.Canvas(
            self.calendar_frame,
            background="#f7f9fc",
            highlightthickness=0,
        )
        self.calendar_scrollbar = ttk.Scrollbar(
            self.calendar_frame,
            orient="vertical",
            command=self.calendar_canvas.yview,
        )
        self.calendar_body = ttk.Frame(self.calendar_canvas)
        self.calendar_body_id = self.calendar_canvas.create_window((0, 0), window=self.calendar_body, anchor="nw")

        self.calendar_canvas.configure(yscrollcommand=self.calendar_scrollbar.set)
        self.calendar_canvas.grid(row=0, column=0, sticky="nsew")
        self.calendar_scrollbar.grid(row=0, column=1, sticky="ns")

        self.calendar_body.bind(
            "<Configure>",
            lambda event: self.calendar_canvas.configure(scrollregion=self.calendar_canvas.bbox("all")),
        )
        self.calendar_canvas.bind(
            "<Configure>",
            lambda event: self.calendar_canvas.itemconfigure(self.calendar_body_id, width=event.width),
        )

        reminder_frame = ttk.LabelFrame(self, text="Reminders", padding=12, style="Reminder.TLabelframe")
        reminder_frame.grid(row=4, column=1, sticky="nsew", padx=(8, 16), pady=(0, 16))
        reminder_frame.columnconfigure(0, weight=1)
        reminder_frame.rowconfigure(0, weight=1)

        form_frame = ttk.Frame(reminder_frame, style="Card.TFrame")
        form_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Date (YYYY-MM-DD):", background="#ffffff").grid(row=0, column=0, sticky="w")
        self.date_var = tk.StringVar(value=self.current_date.strftime("%Y-%m-%d"))
        ttk.Entry(form_frame, textvariable=self.date_var, width=18).grid(row=0, column=1, padx=5, sticky="w")

        ttk.Label(form_frame, text="Reminder:", background="#ffffff").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.reminder_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.reminder_var, width=28).grid(row=1, column=1, padx=5, pady=(8, 0), sticky="w")

        add_button = ttk.Button(form_frame, text="Add Reminder", style="Primary.TButton", command=self.add_reminder)
        add_button.grid(row=2, column=0, columnspan=2, pady=(12, 0), sticky="ew")

        self.message_label = ttk.Label(form_frame, text="", foreground="#d04545", background="#ffffff")
        self.message_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))

        self.reminder_text = tk.Text(
            reminder_frame,
            width=40,
            height=18,
            state="disabled",
            wrap="word",
            padx=10,
            pady=10,
            background="#f8fbff",
            relief="flat",
        )
        self.reminder_text.grid(row=1, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(4, weight=1)

    def on_month_selected(self, event=None):
        selected = self.month_name_var.get()
        if selected in MONTH_NAMES:
            self.month_var.set(MONTH_NAMES.index(selected) + 1)
            self.refresh_calendar()

    def clear_calendar_body(self):
        for child in self.calendar_body.winfo_children():
            child.destroy()

    def refresh_calendar(self):
        year = self.year_var.get()
        month = self.month_var.get()
        view_mode = self.view_mode.get()

        if view_mode == "year":
            self.header_label["text"] = f"All months for {year}"
        else:
            self.header_label["text"] = f"{MONTH_NAMES[month - 1]} {year}"
            self.month_name_var.set(MONTH_NAMES[month - 1])

        self.clear_calendar_body()

        if view_mode == "year":
            self.draw_year_view(year)
        else:
            self.draw_month_view(year, month)

        self.calendar_canvas.yview_moveto(0)

    def draw_month_view(self, year, month):
        month_frame = ttk.LabelFrame(self.calendar_body, text=MONTH_NAMES[month - 1], padding=10)
        month_frame.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")
        self.draw_calendar_grid(month_frame, year, month)

    def draw_year_view(self, year):
        for month_index in range(1, 13):
            row = (month_index - 1) // 3
            col = (month_index - 1) % 3
            month_frame = ttk.LabelFrame(
                self.calendar_body,
                text=MONTH_NAMES[month_index - 1],
                padding=8,
                relief="ridge",
            )
            month_frame.grid(row=row, column=col, padx=8, pady=8, sticky="n")
            self.draw_calendar_grid(month_frame, year, month_index)

    def draw_calendar_grid(self, parent, year, month):
        for col_index, weekday in enumerate(WEEKDAYS):
            label = ttk.Label(parent, text=weekday, style="DayHeader.TLabel", anchor="center", width=3)
            label.grid(row=0, column=col_index, padx=1, pady=2)

        weeks = self.calendar_manager.display_calendar(year, month)
        for row_index, week in enumerate(weeks, start=1):
            row_color = "#f7f9fc" if row_index % 2 == 0 else "#ffffff"
            for col_index, day in enumerate(week):
                label_text = str(day) if day else ""
                label = tk.Label(
                    parent,
                    text=label_text,
                    font=("Segoe UI", 10),
                    bg=row_color,
                    fg="#1f3b5a",
                    width=4,
                    borderwidth=1,
                    relief="solid",
                    padx=4,
                    pady=4,
                )
                if day and year == self.current_date.year and month == self.current_date.month and day == self.current_date.day:
                    label.configure(bg="#ffefd5", fg="#2a4d6e", font=("Segoe UI", 10, "bold"))
                label.grid(row=row_index, column=col_index, padx=1, pady=1)

    def add_reminder(self):
        date_value = self.date_var.get().strip()
        reminder_text = self.reminder_var.get().strip()

        if not date_value or not reminder_text:
            self.set_message("Date and reminder are required.")
            return

        try:
            datetime.strptime(date_value, "%Y-%m-%d")
        except ValueError:
            self.set_message("Please enter the date as YYYY-MM-DD.")
            return

        self.reminder_manager.add_reminder(date_value, reminder_text)
        self.reminder_var.set("")
        self.set_message("Reminder added.", "green")
        self.refresh_reminder_list()

    def refresh_reminder_list(self):
        reminders = []
        for date in sorted(self.reminder_manager.reminders):
            reminders.append(f"{date}:")
            for item in self.reminder_manager.get_reminders(date):
                reminders.append(f"  - {item}")
            reminders.append("")

        content = "\n".join(reminders) if reminders else "No reminders yet."
        self.reminder_text.configure(state="normal")
        self.reminder_text.delete("1.0", "end")
        self.reminder_text.insert("end", content)
        self.reminder_text.configure(state="disabled")

    def set_message(self, text, color="red"):
        self.message_label["text"] = text
        self.message_label["foreground"] = color


def main():
    app = CalendarReminderApp()
    app.mainloop()


if __name__ == "__main__":
    main()
