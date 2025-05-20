from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('save_comment/', views.save_comment, name='save_comment'),
    path('comment/<int:comment_id>/reply/', views.save_reply, name='save_reply'),
	path('category/<slug:slug>/', views.post_list_by_category, name='post_list_by_category'),
]