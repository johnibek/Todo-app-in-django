from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileDetail.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEdit.as_view(), name='profile-edit'),
]