from django.urls import path
from Blog_App import views

app_name = 'Blog_App'
urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('create-post/', views.CreatePost.as_view(), name='create_post'),
    path('Post-details/<slug:slug>', views.post_details, name='post_details'),
    path('liked/<pk>/', views.liked, name='liked_post'),
    path('unliked/<pk>/', views.unliked, name='unliked_post'),
    path('edit-post/<pk>/', views.EditPost.as_view(), name='edit_post'),
    path('delete-post/<pk>/', views.DeletePost.as_view(), name= 'delete_post'),
]
