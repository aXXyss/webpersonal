from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('servicios/', views.servicios, name='servicios'),
    path('infraestructura/', views.infraestructura, name='infraestructura'),
    path('fuelaxflow/', views.fuelaxflow, name='fuelaxflow'),
    path('demos/', views.demos, name='demos'),
]