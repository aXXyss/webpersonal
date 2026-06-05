from django.urls import path
from comments import views

app_name = 'comments'

urlpatterns = [
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]