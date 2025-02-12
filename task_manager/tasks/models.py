from django.db import models
from django.contrib.auth.models import User  # Import User model for task ownership

# Define Task model
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)  # Task title
    description = models.TextField()  # Task description
    due_date = models.DateField()  # Task due date
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Task status
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate task with a user

    def __str__(self):
        return self.title  # Show task title in Django Admin
