from django.urls import path
from . import views
from .views import register

urlpatterns = [
    path('', views.task_list, name='task_list'),  # List all tasks
    path('<int:task_id>/', views.task_detail, name='task_detail'),  # Task details
    path('create/', views.task_create, name='task_create'),  # Create task
    path('<int:task_id>/edit/', views.task_edit, name='task_edit'),  # Edit task
    path('<int:task_id>/delete/', views.task_delete, name='task_delete'),  # Delete task
    path("register/", register, name="register"),
    path('mark_as_completed/<int:task_id>/', views.mark_as_completed, name='mark_as_completed'),
    path('', views.home, name='home'), # Home page
    path('tasks/', views.task_list, name='task_list'),  # Task list
]
