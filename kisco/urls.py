from django.urls import path

from kisco.views import views

urlpatterns = [
    # 메인화면
    path('', views.IndexView.as_view(), name='index'),
]
