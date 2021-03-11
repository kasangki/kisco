from django.urls import path

from kisco.views import views
from kisco.views.steel_out_var import *

urlpatterns = [
    # 메인화면
    path('', views.IndexView.as_view(), name='index'),

    # 주요데이터분석 출강량
    path('steel_out_var', SteelOutVarView.as_view(), name='steel_out_var'),
]
