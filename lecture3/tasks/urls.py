from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    # Add your task-related URL patterns here
    # Example: path('', views.index, name='index'),
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('update/<int:task_index>', views.update, name='update'),
    path('delete/<int:task_index>', views.delete, name='delete'),
    path('clear-all', views.clear_all, name='clear_all'),
] 