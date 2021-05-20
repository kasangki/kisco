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

        # 작업지시할 작업 조회
    def make_work_direct(request):
        target_code = request.POST.get('target_code')
        target_value = request.POST.get('target_value')
        op_num = request.POST.get('op_num')

        smartTopSum = TbSmartopSum.objects.filter(op_num=op_num).values()
        smart_top_sum_df = pd.DataFrame(list(smartTopSum))
        smart_top_sum_df.drop(['op_num','create_dtm','update_dtm'],axis=1,inplace=True)





        ## 상위 몇 퍼센터 가져오기 시작
        count = len(smart_top_sum_df)
        target_value = int(target_value)

        value_dict = ''
        high_rank = int((target_value / 100) * count)
        if (target_value == 100):
            value_dict = smart_top_sum_df.loc[len(smart_top_sum_df) - 1].to_dict()  # 검색된 Series
        else:
            value_dict = smart_top_sum_df.loc[high_rank].to_dict()  # 검색된 Series

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
            'high_rank': high_rank,
            'ttt_var_list': ttt_var_list,
            'steel_var_list': steel_var_list,
            'mat_var_list': mat_var_list,
            'equip_var_list': equip_var_list,
            'etc_var_list': etc_var_list,
        }

        return HttpResponse(json.dumps(context), content_type="application/json")





