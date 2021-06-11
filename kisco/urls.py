from django.urls import path

from kisco.views import views
from kisco.views.steel_out_var import *
from kisco.views.analytic_single_var import *
from kisco.views.predict_analytic import *
from kisco.views.work_direct import *
from kisco.views.work_direct_history import *

urlpatterns = [
    # 메인화면
    path('', views.IndexView.as_view(), name='index'),
    path('index2/<int:arg1>', views.Index2View.as_view(), name='index2'),
    path('<int:target_value_code_num>', views.IndexMainDataAna.as_view(), name='main_data_ana'),

    # 주요데이터분석 출강량
    path('steel_out_var', SteelOutVarView.as_view(), name='steel_out_var'),


    path('analytic_single_var', AnalyticSingleVarView.analytic_single_var, name='analytic_single_var'),
    path('power_factor', AnalyticSingleVarView.power_factor, name='power_factor'),
    path('predict_analytic/<int:target_value_code_num>', PredictAnalyticView.as_view(), name='predict_analytic'),
    path(r'^predict_analytic/(?P<target_value_code>[-\w]+)/$', PredictAnalyticView.as_view(), name='predict_analytic'),


    path('search_operate_number', SearchOperateNumberView.as_view(), name='search_operate_number'),
    path('search_optimal_predict', SearchOptimalPredictView.as_view(), name='search_optimal_predict'),
    path('search_var_info', SearchVarInfoView.as_view(), name='search_var_info'),
    path('search_var_list', SearchVarInfoView.as_view(), name='search_var_list'),

    # 작업지시_1
    path('work_direct_manager',WorkDirectManagerView.as_view(), name='work_direct_manager'),
    path('search_work',WorkDirectManagerView.search_work, name='search_work'),
    path('make_work_direct',WorkDirectManagerView.make_work_direct, name='make_work_direct'),
    
    # 작업지시_2
    path('work_direct_manager_history',WorkDirectManagerHistoryView.as_view(), name='work_direct_manager_history'),
    path('search_work_history',WorkDirectManagerHistoryView.search_work_history, name='search_work_history'),
    path('make_work_direct_history',WorkDirectManagerHistoryView.make_work_direct_history, name='make_work_direct_history'),

    # 모델생성
    path('make_model', TrainModelViews.make_model, name='make_model'),
]
