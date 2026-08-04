from django.urls import path
from . import views

app_name = 'helpdesk'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('verify/', views.verify_turnstile, name='verify'),
]