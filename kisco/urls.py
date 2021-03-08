from django.urls import path



urlpatterns = [
    # 메인화면
    path('', views.IndexView.as_view(), name='index'),
]
