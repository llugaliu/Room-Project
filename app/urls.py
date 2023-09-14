from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up/', views.signup, name='signup'),
    path('login/', auth_view.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('edit-room/<str:pk>/', views.edit_room, name='edit-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('edit-profile/<str:pk>/', views.edit_profile, name='edit-profile')
]
