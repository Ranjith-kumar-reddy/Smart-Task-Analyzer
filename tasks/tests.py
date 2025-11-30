from datetime import date, timedelta
from django.test import SimpleTestCase
from .scoring import calculate_task_score


class TaskScoringTests(SimpleTestCase):
    def test_overdue_task_gets_big_boost(self):
        task = {
            "title": "Overdue task",
            "due_date": (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "importance": 5,
            "estimated_hours": 3,
        }
        score = calculate_task_score(task)

        # Should be very high because overdue => +100
        self.assertGreaterEqual(score, 100)

    def test_due_soon_task_gets_medium_boost(self):
        task = {
            "title": "Due soon task",
            "due_date": (date.today() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "importance": 5,
            "estimated_hours": 3,
        }
        score = calculate_task_score(task)

        # Due in <= 3 days => +50
        
        self.assertGreaterEqual(score, 50)

    def test_far_future_task_has_no_urgency_bonus(self):
        task = {
            "title": "Future task",
            "due_date": (date.today() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "importance": 5,
            "estimated_hours": 3,
        }
        score = calculate_task_score(task)

        # No overdue / soon bonus, just importance * 5

        expected_min = 5 * 5  # importance * 5
        self.assertGreaterEqual(score, expected_min)

    def test_missing_importance_uses_default(self):
        task = {
            "title": "No importance",
            "due_date": (date.today() + timedelta(days=5)).strftime("%Y-%m-%d"),
            # no "importance" key
            "estimated_hours": 3,
        }
        score = calculate_task_score(task)

        # Default importance in scoring is 5, so at least 25 points from importance 
        self.assertGreaterEqual(score, 25)

    def test_quick_task_gets_extra_bonus(self):
        base_task = {
            "title": "Normal task",
            "due_date": (date.today() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "importance": 5,
            "estimated_hours": 3,
        }
        quick_task = {
            **base_task,
            "estimated_hours": 1,  # quick win < 2 hours
        }

        base_score = calculate_task_score(base_task)
        quick_score = calculate_task_score(quick_task)

        self.assertGreater(quick_score, base_score)

    def test_string_due_date_parsing_works(self):

        # Just ensure no crash when passing string date type 
        task = {
            "title": "String date",
            "due_date": date.today().strftime("%Y-%m-%d"),
            "importance": 5,
            "estimated_hours": 2,
        }
        score = calculate_task_score(task)

        # Just checking it returns an int
        self.assertIsInstance(score, int)
