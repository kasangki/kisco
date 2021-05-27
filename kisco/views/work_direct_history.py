'''
 * Created by : 강상기
 * Created Date : 2021. 5 .17
 * author 강상기
 * 내용 : 작업지시 - 관리자
 */
'''
import psycopg2.extras
from django.shortcuts import render
from django.views.generic import TemplateView
from kisco.models import TbSmartopSum, TbVarMap, TbTargetValue
from django.db.models import Max


import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.model_selection import train_test_split

from django.http import HttpResponse, JsonResponse
import simplejson as json
from statsmodels.stats.outliers_influence import variance_inflation_factor
from kisco.anaytics.value_select import ValueSelect
import time
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import itertools
import pickle
import joblib

from kisco.models import TbModel
from kisco.models import TbVarInfo
from datetime import datetime

from django.forms.models import model_to_dict

from kisco.anaytics.smart_operate_report import SmartOperateReport
from kisco.anaytics.db_util import DBUtil
from kisco.views.views import IndexView
from kisco.anaytics.quantile_analytics import QuantileAnalytics
from django.db import connection


# 생성된 모델 예측
class WorkDirectManagerHistoryView(TemplateView):
    def get(self, request, *args, **kwargs):

        smartop_sum = TbSmartopSum.objects.aggregate(op_num=Max('op_num'))
        op_num  = str(smartop_sum['op_num'])
        db_util = DBUtil()
        flag = 'single'
        smartop_sum_list = db_util.get_smartop_sum_list(op_num,flag)
        smartop_sum_dict = db_util.convert_to_dict(smartop_sum_list)


        #return var_info_list
        print(smartop_sum_dict)
        context = {
            'smartop_sum_dict' : smartop_sum_dict,
                   }
        return render(request, 'work_direct_history/index.html', context=context)


    # 작업지시할 작업 조회
    def search_work_history(request):

        # smartop_sum = TbSmartopSum.objects.aggregate(op_num=Max('op_num'))
        # op_num = smartop_sum['op_num']
        op_num = request.POST.get('op_num')
        flag = 'single'
        db_util = DBUtil()
        smartop_sum_list = db_util.get_smartop_sum_list(op_num,flag)
        smartop_sum_dict = db_util.convert_to_dict(smartop_sum_list)


        # return var_info_list
        print(smartop_sum_dict)
        context = {
            'smartop_sum_dict': smartop_sum_dict,
        }
        return HttpResponse(json.dumps(context), content_type="application/json")



    # 작업지시할 작업 생성
    def make_work_direct_history(request):
        target_code = request.POST.get('target_code')
        #target_value = request.POST.get('target_value')
        op_num = request.POST.get('op_num')

        var_list = request.POST.getlist('var_list[]')   # 변수목록
        var_name_list = request.POST.getlist('var_name_list[]')   # 변수명 리스트
      
        db_util = DBUtil()

        # 예측할 데이터
        flag = 'single'
        smartop_sum_list = db_util.get_smartop_sum_list(op_num,flag)
        smartop_sum_dict = db_util.convert_to_dict(smartop_sum_list)
        smart_top_sum_df = pd.DataFrame(smartop_sum_dict)
        smart_top_sum_df.drop(['op_num','create_dtm','update_dtm'],axis=1,inplace=True)
        
        
        # 학습대상 전체 데이터
        smartop_sum_all_list = db_util.get_smartop_sum_list(op_num, 'all')
        smart_op_sum_all_dict = db_util.convert_to_dict(smartop_sum_all_list)
        smart_op_sum_all_df = pd.DataFrame(smart_op_sum_all_dict)
        # 변수선택용 dataframe 가져온다. 조회된 dataframe은 그대로 가져온다.
        smart_op_sum_all_value_df = smart_op_sum_all_df.drop(['op_num','create_dtm','update_dtm'], axis=1, inplace=False)



        # 학습데이터, 테스트 데이터 분리
        #smart_op_sum_all_value_df = sm.add_constant(smart_op_sum_all_value_df,has_constant='add')
        feature_columns = list(smart_op_sum_all_value_df.columns.difference([target_code]))
        X = smart_op_sum_all_value_df[feature_columns]
        y = smart_op_sum_all_value_df[target_code]
        train_x, test_x, train_y, test_y = train_test_split(X, y, train_size=0.7, test_size=0.3)
        
        


        ## RandomForestRegressor 알고리즘 적용
        model = RandomForestRegressor(n_estimators=100, max_depth=100)
        # RandomForestRegressor 학습시작
        model.fit(train_x, train_y)


        X_ex_test = smart_top_sum_df[feature_columns]
        y_ex_test = smart_top_sum_df[target_code]

        ttt = np.array(X_ex_test.values.tolist())

        # 최종예측결과
        predict_ex_test = model.predict(ttt)
        print(predict_ex_test)



        # 전체변수목록
        all_var_name = TbVarMap.objects.exclude(var_code='op_num').values()
        all_var_name_df = pd.DataFrame(list(all_var_name))
        all_var_name_df.sort_values('seq')

        all_var_name_list = list(all_var_name_df['var_name'])
        all_var_code_list = list(all_var_name_df['var_code'])
        var_list = []
        for i in range(len(all_var_code_list)):
            temp = [all_var_code_list[i], all_var_name_list[i]]
            var_list.append(temp)

        #value_dict = smart_top_sum_df.to_dict()
        # smartop_sum_dict.pop('op_num')
        # smartop_sum_dict.pop('create_dtm')
        # smartop_sum_dict.pop('update_dtm')
        #value_dict = smartop_sum_dict
        del smartop_sum_dict[0]['op_num']
        del smartop_sum_dict[0]['create_dtm']
        del smartop_sum_dict[0]['update_dtm']
        value_dict = smartop_sum_dict[0]
        print(value_dict)
        db_util = DBUtil()
        ttt_var_list = db_util.set_y_final_all_value_list('T', all_var_name_df, value_dict,
                                                          all_var_code_list)  ## 시간변수목록
        steel_var_list = db_util.set_y_final_all_value_list('S', all_var_name_df, value_dict,
                                                            all_var_code_list)  ## 고철종류 변수목록
        mat_var_list = db_util.set_y_final_all_value_list('M', all_var_name_df, value_dict,
                                                          all_var_code_list)  ## 부자재 변수목록
        equip_var_list = db_util.set_y_final_all_value_list('Q', all_var_name_df, value_dict,
                                                            all_var_code_list)  ## 설비변수 목록
        etc_var_list = db_util.set_y_final_all_value_list('E', all_var_name_df, value_dict,
                                                          all_var_code_list)  ## 기타 변수 목록
        ##data_list = smart_top_sum_df[feature_columns]
        ## 상위 몇 퍼센터 가져오기 끝

        context = {
            'predict_y_value' : str(predict_ex_test[0]),
            'ttt_var_list': ttt_var_list,
            'steel_var_list': steel_var_list,
            'mat_var_list': mat_var_list,
            'equip_var_list': equip_var_list,
            'etc_var_list': etc_var_list,
            'op_num': str(op_num),
        }

        return HttpResponse(json.dumps(context), content_type="application/json")



