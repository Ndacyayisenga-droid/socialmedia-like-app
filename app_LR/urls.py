from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexReg),
    path('log', views.indexLog),
    path('success', views.success),
    path('Profile_name', views.ProName),
    path('Register', views.register),
    path('Login', views.login),
    path('Logout', views.logout),
]