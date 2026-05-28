class ReminderManager:
    def __init__(self):
        self.reminders = {}

    def add_reminder(self, date, reminder):
        if date in self.reminders:
            self.reminders[date].append(reminder)
        else:
            self.reminders[date] = [reminder]

    def get_reminders(self, date):
        return self.reminders.get(date, [])