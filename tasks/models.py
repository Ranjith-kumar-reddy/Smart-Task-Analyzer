from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    importance = models.IntegerField(default=5)  # 1–10
    estimated_hours = models.IntegerField(default=1)
    dependencies = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title
