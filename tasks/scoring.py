from datetime import date, datetime

def calculate_task_score(task_data):
    """
    Calculates a priority score.
    Higher score = Higher priority.
    """
    score = 0
    today = date.today()

    
    due = task_data.get("due_date")
    if isinstance(due, str):
        due = datetime.strptime(due, "%Y-%m-%d").date()
    days_until_due = (due - today).days

    if days_until_due < 0:
        score += 100  # overdue
    elif days_until_due <= 3:
        score += 50   # due soon

    
    importance = task_data.get("importance", 5)
    score += importance * 5

    estimated_hours = task_data.get("estimated_hours", 1)
    if estimated_hours < 2:
        score += 10

    return score
