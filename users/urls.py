from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    # path('login_01/', views.login_01),
    path('logout/', views.logout),
    path('user_list/', views.users_list,name='user_list'),
    path('register/', views.register),
    path('user_update/', views.user_update,name='user_update'),
    path('user_delete/P(?P<str:pk>[^/]+)$', views.user_delete,name='user_delete'),
    path('user_detail/P(?P<str:pk>[^/]+)$', views.user_detail,name='user_detail'),

]