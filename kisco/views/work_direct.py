'''
 * Created by : 강상기
 * Created Date : 2021. 5 .17
 * author 강상기
 * 내용 : 작업지시 - 관리자
 */
'''

from django.shortcuts import render
from django.views.generic import TemplateView
from kisco.models import TbSmartopSum, TbVarMap, TbTargetValue

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
class WorkDirectManagerView(TemplateView):
    def get(self, request, *args, **kwargs):
        # target_value_code = kwargs['target_value_code']
        #
        # # 타겟변수명 조회
        # var_map_instance = TbVarMap.objects.get(var_code=target_value_code)
        # target_value_name = var_map_instance.var_name
        #
        # # 모델목록 조회
        # model = TbModel.objects.filter(target_code=target_value_code).values()
        # model_list = list(model)
        # print(model_list)

        context = {
                   }
        return render(request, 'work_direct/index.html', context=context)

    # 작업지시할 작업 조회
    def search_work(request):
        target_code = request.POST.get('target_code')
        target_value = request.POST.get('target_value')


        smartTopSum = TbSmartopSum.objects.all().order_by(target_code).values()
        smart_top_sum_df = pd.DataFrame(list(smartTopSum))

        ## 상위 몇 퍼센터 가져오기 시작 
        count = len(smart_top_sum_df)
        target_value = int(target_value)

        value_dict = ''
        high_rank = int((target_value / 100) * count)
        if(target_value == 100) :
            value_dict = smart_top_sum_df.loc[len(smart_top_sum_df)-1].to_dict() # 검색된 Series
        else :
            value_dict = smart_top_sum_df.loc[high_rank].to_dict()  # 검색된 Series

        op_num = value_dict['op_num']
        #전체변수목록
        all_var_name = TbVarMap.objects.exclude(var_code = 'op_num').values()
        all_var_name_df = pd.DataFrame(list(all_var_name))
        all_var_name_df.sort_values('seq')

        all_var_name_list = list(all_var_name_df['var_name'])
        all_var_code_list = list(all_var_name_df['var_code'])
        var_list = []
        for i in range(len(all_var_code_list)):
            temp = [all_var_code_list[i], all_var_name_list[i]]
            var_list.append(temp)


        db_util = DBUtil()
        ttt_var_list = db_util.set_y_final_all_value_list('T', all_var_name_df,value_dict,all_var_code_list)  ## 시간변수목록
        steel_var_list = db_util.set_y_final_all_value_list('S', all_var_name_df,value_dict,all_var_code_list)  ## 고철종류 변수목록
        mat_var_list = db_util.set_y_final_all_value_list('M', all_var_name_df,value_dict,all_var_code_list)  ## 부자재 변수목록
        equip_var_list = db_util.set_y_final_all_value_list('Q', all_var_name_df,value_dict,all_var_code_list)  ## 설비변수 목록
        etc_var_list = db_util.set_y_final_all_value_list('E', all_var_name_df,value_dict,all_var_code_list)  ## 기타 변수 목록

        ##data_list = smart_top_sum_df[feature_columns]
        ## 상위 몇 퍼센터 가져오기 끝


        context = {
             'high_rank' : high_rank,
            'ttt_var_list': ttt_var_list,
            'steel_var_list': steel_var_list,
            'mat_var_list': mat_var_list,
            'equip_var_list': equip_var_list,
            'etc_var_list': etc_var_list,
            'op_num' : str(op_num),
        }


        return HttpResponse(json.dumps(context), content_type="application/json")




    # 작업지시할 작업 생성
    def make_work_direct(request):
        target_code = request.POST.get('target_code')
        target_value = request.POST.get('target_value')
        op_num = request.POST.get('op_num')

        # 예측할 데이터
        smartTopSum = TbSmartopSum.objects.filter(op_num=op_num).values()
        smart_top_sum_df = pd.DataFrame(list(smartTopSum))
        smart_top_sum_df.drop(['op_num','create_dtm','update_dtm'],axis=1,inplace=True)



        smart_op_sum_all = TbSmartopSum.objects.all().values()
        smart_op_sum_all_df = pd.DataFrame(list(smart_op_sum_all))

        # 변수선택용 dataframe 가져온다. 조회된 dataframe은 그대로 가져온다.
        smart_op_sum_all_value_df = smart_op_sum_all_df.drop(['op_num','create_dtm','update_dtm'], axis=1, inplace=False)

        smart_op_sum_all_value_df = sm.add_constant(smart_op_sum_all_value_df,has_constant='add')
        feature_columns = list(smart_op_sum_all_value_df.columns.difference([target_code]))
        X = smart_op_sum_all_value_df[feature_columns]
        y = smart_op_sum_all_value_df[target_code]
        train_x, test_x, train_y, test_y = train_test_split(X, y, train_size=0.7, test_size=0.3)

        vif = pd.DataFrame()
        vif["VIF Factor"] = [variance_inflation_factor(smart_op_sum_all_value_df.values, i) for i in range(smart_op_sum_all_value_df.shape[1])]
        vif["features"] = smart_op_sum_all_value_df.columns
        print(vif)

        value_select = ValueSelect()
        model_info_aic = value_select.process_subset(X=train_x,y=train_y,feature_set=feature_columns)
        print(model_info_aic)

        # getBest: 가장 낮은 AIC를 가지는 모델 선택 및 저장
        best_model = value_select.get_best(X=train_x, y=train_y, k=2)
        print(best_model)

        # 변수 선택에 따른 학습시간과 저장
        models = pd.DataFrame(columns=["AIC", "model"])
        tic = time.time()
        for i in range(1, 4):
            models.loc[i] = value_select.get_best(X=train_x, y=train_y, k=i)
        toc = time.time()
        print("Total elapsed time:", (toc - tic), "seconds.")

        Forward_best_model = value_select.forward_model(X=train_x, y=train_y)
        print(Forward_best_model.summary())

        coef_values_dict = Forward_best_model.params.to_dict()
        print(coef_values_dict)
        coef_values_list = list(coef_values_dict.keys())

        del coef_values_list[coef_values_list.index('const')]
        #coef_values_list.append(target_code)   # target_code 추가

        ## RandomForestRegressor 알고리즘 적용
        model = RandomForestRegressor(n_estimators=100, max_depth=100)
        train_x = train_x[coef_values_list]
        # RandomForestRegressor 학습시작
        model.fit(train_x, train_y)


        X_ex_test = smart_top_sum_df[coef_values_list]
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

        value_dict = smart_top_sum_df.to_dict()
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



