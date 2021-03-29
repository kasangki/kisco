from django.urls import path

from kisco.views import views
from kisco.views.steel_out_var import *
from kisco.views.analytic_single_var import *

urlpatterns = [
    # 메인화면
    path('', views.IndexView.as_view(), name='index'),
    path('index2', views.Index2View.as_view(), name='index2'),

    # 주요데이터분석 출강량
    path('steel_out_var', SteelOutVarView.as_view(), name='steel_out_var'),

    path('analytic_single_var', AnalyticSingleVarView.analytic_single_var, name='analytic_single_var'),
    path('make_model', AnalyticSingleVarView.make_model, name='make_model'),
]
