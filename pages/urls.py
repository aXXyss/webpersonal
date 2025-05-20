from django.urls import path
from .import views

urlpatterns = [
    path('<int:page_id>/<slug:page_slug>/', views.page, name='page'),    #  <int:page_id> el INT convierte en Integer la cadena de exto
]