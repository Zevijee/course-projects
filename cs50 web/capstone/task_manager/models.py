from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Task(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='task')
    text = models.TextField(blank=False)
    time = models.TimeField()
    date_todo_on = models.DateField()
    urgency = models.IntegerField()
    completed = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "time": self.time,
            "date_todo_on": self.date_todo_on,
            "urgency": self.urgency,
            "completed": self.completed
        }

    def __str__(self):
        return f"{self.text} made on {self.date_todo_on} id = {self.id}"

