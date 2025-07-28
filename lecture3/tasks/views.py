from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages

# Create your views here.

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task", widget=forms.TextInput(attrs={'placeholder': 'Enter task description'}))
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=7, initial=1)


class UpdateTaskForm(forms.Form):
    task = forms.CharField(label="Task", widget=forms.TextInput(attrs={'placeholder': 'Enter task description'}))
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=7)


def _get_tasks_session(request):
    """Helper function to get or initialize tasks session."""
    if "tasks" not in request.session:
        request.session["tasks"] = []
    
    # Clean up corrupted data
    tasks = request.session["tasks"]
    cleaned_tasks = []
    
    for task in tasks:
        if isinstance(task, dict) and "task" in task and task["task"].strip():
            # Ensure priority is valid
            priority = task.get("priority", 1)
            if not isinstance(priority, int) or priority < 1 or priority > 7:
                priority = 1
            
            cleaned_tasks.append({
                "task": task["task"].strip(),
                "priority": priority
            })
    
    # Update session with cleaned data
    request.session["tasks"] = cleaned_tasks
    return cleaned_tasks


def index(request):
    """Display all tasks."""
    tasks = _get_tasks_session(request)
    return render(request, 'tasks/index.html', {"tasks": tasks})


def add(request):
    """Add a new task."""
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data["task"].strip()
            priority = form.cleaned_data.get("priority", 1)
            
            # Validate task name
            if not task_name:
                messages.error(request, 'Task name cannot be empty.')
                return render(request, 'tasks/add.html', {"form": form})
            
            # Add task to session
            tasks = _get_tasks_session(request)
            tasks.append({"task": task_name, "priority": priority})
            
            messages.success(request, f'Task "{task_name}" added successfully!')
            return redirect("tasks:index")
        else:
            return render(request, 'tasks/add.html', {"form": form})
    
    return render(request, 'tasks/add.html', {"form": NewTaskForm()})


def update(request, task_index):
    """Update an existing task."""
    tasks = _get_tasks_session(request)
    
    # Validate task index
    if not (0 <= task_index < len(tasks)):
        messages.error(request, 'Task not found.')
        return redirect('tasks:index')
    
    task = tasks[task_index]
    
    if request.method == "POST":
        form = UpdateTaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data["task"].strip()
            priority = form.cleaned_data.get("priority", 1)
            
            # Validate task name
            if not task_name:
                messages.error(request, 'Task name cannot be empty.')
                return render(request, 'tasks/update.html', {
                    "form": form,
                    "task": task,
                    "task_index": task_index
                })
            
            # Update the task
            old_task_name = task["task"]
            tasks[task_index] = {"task": task_name, "priority": priority}
            
            messages.success(request, f'Task "{old_task_name}" updated to "{task_name}" successfully!')
            return redirect("tasks:index")
        else:
            return render(request, 'tasks/update.html', {
                "form": form,
                "task": task,
                "task_index": task_index
            })
    
    # GET request - show update form with current values
    form = UpdateTaskForm(initial={
        "task": task["task"],
        "priority": task["priority"]
    })
    
    return render(request, 'tasks/update.html', {
        "form": form,
        "task": task,
        "task_index": task_index
    })


def delete(request, task_index):
    """Delete a task by index."""
    tasks = _get_tasks_session(request)
    
    # Validate task index
    if not (0 <= task_index < len(tasks)):
        messages.error(request, 'Task not found.')
        return redirect('tasks:index')
    
    task = tasks[task_index]
    
    if request.method == "POST":
        # Delete the task
        task_name = task["task"]
        del tasks[task_index]
        
        messages.success(request, f'Task "{task_name}" deleted successfully!')
        return redirect('tasks:index')
    
    # GET request - show confirmation page
    return render(request, 'tasks/delete.html', {
        "task": task,
        "task_index": task_index
    })


def clear_all(request):
    """Clear all tasks."""
    if request.method == "POST":
        request.session["tasks"] = []
        messages.success(request, 'All tasks cleared successfully!')
        return redirect('tasks:index')
    
    return redirect('tasks:index')