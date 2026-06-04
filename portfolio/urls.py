from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('project/', views.project_list, name='project_list'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
]