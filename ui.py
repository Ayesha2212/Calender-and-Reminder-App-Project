import calendar

def show_calendar(calendar_data):
    print("Mo Tu We Th Fr Sa Su")

    for week in calendar_data:
        for day in week:
            if day == 0:
                print("   ", end=" ")  
            else:
                print(f"{day:2}", end=" ")
        print()


def prompt_for_reminder():
    date = input("Enter the date for the reminder (YYYY-MM-DD): ")
    reminder = input("Enter the reminder: ")
    return date, reminder