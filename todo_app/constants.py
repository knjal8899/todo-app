from datetime import timedelta

REMINDER_TIME_DELTA = timedelta(minutes=15)


PRIORITY_CHOICES = [("HIGH", "High"), ("MEDIUM", "Medium"), ("LOW", "Low")]


STATUS_CHOICES = [
    ("TODO", "Todo"),
    ("INPROGRESS", "In Progress"),
    ("COMPLETED", "Completed"),
]
