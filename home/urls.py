from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('About/', views.About, name='About'),
    path('Contact/', views.contact, name='Contact'),
    path('CharitySignUpPage/', views.CharitySignUpPage, name='CharitySignUpPage'),
    path('CharitySignUp/', views.CharitySignUp, name='CharitySignUp'),
    path('DonorSignUpPage/', views.DonorSignUpPage, name='DonorSignUpPage'),
    path('DonorSignUp/', views.DonorSignUp, name='DonorSignUp'),
    path('LoginPage/', views.LoginPage, name='LoginPage'),
    path('Login/', views.Login, name='Login'),
    path('Logout/',views.Logout, name="Logout"),
    path('Charity/<str:slug>',views.Charity, name="Charity"),
    path('Payment/',views.Payment,name = 'Payment'),
    path('Message/',views.Message,name = 'Message')
]