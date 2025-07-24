from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('mahmoud/', views.mahmoud, name='mahmoud'),  # Mahmoud's page
    path('dream/', views.dream, name='dream'),  # Dream page
    path('<str:name>/', views.greet, name='greet'),  # Personalized greeting page
]



