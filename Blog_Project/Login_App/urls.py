from django.urls import path
from Login_App import views



app_name = 'Login_App'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('password/', views.password_change, name='password_change'),
    path('add-profilepic/', views.add_profile_Image, name='add_profile_Image'),
    path('change-profilepic/', views.change_profile_image, name='change_profile_image'),
]
