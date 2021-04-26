from django.urls import path

from kisco.views import views
from kisco.views.steel_out_var import *
from kisco.views.analytic_single_var import *
from kisco.views.predict_analytic import *

urlpatterns = [
    # 메인화면
    path('', views.IndexView.as_view(), name='index'),
    path('index2/<int:arg1>', views.Index2View.as_view(), name='index2'),
    path('main_data_ana/<int:target_value_code_num>', views.IndexMainDataAna.as_view(), name='main_data_ana'),

    # 주요데이터분석 출강량
    path('steel_out_var', SteelOutVarView.as_view(), name='steel_out_var'),

    path('analytic_single_var', AnalyticSingleVarView.analytic_single_var, name='analytic_single_var'),
    path('power_factor', AnalyticSingleVarView.power_factor, name='power_factor'),
    path('predict_analytic/<int:target_value_code_num>', PredictAnalyticView.as_view(), name='predict_analytic'),
    path(r'^predict_analytic/(?P<target_value_code>[-\w]+)/$', PredictAnalyticView.as_view(), name='predict_analytic'),
    path('search_opeate_number', SearchOperateNumberView.as_view(), name='search_opeate_number'),
    path('search_optimal_predict', SearchOptimalPredictView.as_view(), name='search_optimal_predict'),


    path('make_model', AnalyticSingleVarView.make_model, name='make_model'),
]
