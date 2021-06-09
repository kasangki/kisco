from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report,name='report'),
    path('search_report/', views.search_report,name='search_report'),
]