from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('user_list/', views.users_list),
]