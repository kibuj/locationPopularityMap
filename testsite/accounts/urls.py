from django.urls import path
from . import views

urlpatterns = [
    # /api/accounts/register/
    path('register/', views.RegisterView.as_view(), name='register'),

    # /api/accounts/login/
    path('login/', views.LoginView.as_view(), name='login'),

    # /api/accounts/logout/
    path('logout/', views.LogoutView.as_view(), name='logout'),


]