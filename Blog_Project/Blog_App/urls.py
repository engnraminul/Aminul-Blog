from django.urls import path
from Blog_App import views

app_name = 'Blog_App'
urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('create-post/', views.CreatePost.as_view(), name='create_post'),
    path('details/<slug:slug>', views.post_details, name='post_details'),
    path('liked/<pk>/', views.liked, name='liked_post'),
    path('unliked/<pk>/', views.unliked, name='unliked_post'),
]
