from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('eid-fitr/', views.eid_el_fitr, name='eid_el_fitr'),
    path('eid-adha/', views.eid_el_adha, name='eid_el_adha'),
    path('ramadan/', views.ramadan, name='ramadan'),
]
