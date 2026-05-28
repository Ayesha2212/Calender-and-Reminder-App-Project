import calendar


class CalendarManager:

    def display_calendar(self, year, month):
        return calendar.monthcalendar(year, month)

    def get_days_in_month(self, year, month):
        return calendar.monthrange(year, month)[1]
