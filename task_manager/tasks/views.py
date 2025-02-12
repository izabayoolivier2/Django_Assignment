from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from django.db.models import Q
from .forms import TaskForm
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.http import HttpResponseForbidden


#the Registration View
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash the password
            user.save()
            login(request, user)  # Log in after registration
            return redirect("task_list")  # Redirect to task list
    else:
        form = UserRegistrationForm()
    
    return render(request, "tasks/register.html", {"form": form})


# Display all tasks for the logged-in user
@login_required
def task_list(request):
    query = request.GET.get('q', '')  # Get search query for title
    status_filter = request.GET.get('status', '')  # Get status filter

    tasks = Task.objects.filter(user=request.user)  # Show only the logged-in user's tasks

    # Apply title filter if query exists
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |  # Filter by title (case insensitive)
            Q(description__icontains=query)  # Filter by description (case insensitive)
        )
    
    # Apply status filter if selected
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'query': query, 'status_filter': status_filter})




# Show details of a specific task
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

# Create a new task
@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the logged-in user
            task.save()
            return redirect('task_list')  # Redirect to task list
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})



# Edit an existing task
@login_required
def task_edit(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.user != request.user:  # Restrict access
        return HttpResponseForbidden("You are not allowed to edit this task.")

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {"form": form})


# Delete a task
@login_required
def task_delete(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.user != request.user:  # Restrict access
        return HttpResponseForbidden("You are not allowed to delete this task.")

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tasks/task_confirm_delete.html", {"task": task})



#view to handle marking a task as completed
def mark_as_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure task belongs to the logged-in user
    task.status = 'Completed'  # Mark task as completed
    task.save()  # Save the task

    return redirect('task_list')  # Redirect back to the task list


#the Home Page View
def home(request):
    return render(request, 'tasks/home.html')  # Render the home page