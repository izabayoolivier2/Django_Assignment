from django.contrib import admin
from .models import Task  # Import Task model

admin.site.register(Task)  # Register Task model in admin panel

