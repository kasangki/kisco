
'''
 * Created by : 강상기
 * Created Date : 2021. 3 .10
 * author 강상기
 * 내용 : 주요데이터분석 - 싱글변수
 */
'''

from django.shortcuts import render
from django.views.generic import TemplateView
from kisco.models import TbSmartopSum, TbVarMap
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
from kisco.anaytics.quantile_analytics import QuantileAnalytics

class PredictAnalyticView(TemplateView):
    def get(self, request, *args, **kwargs):

        target_value_code = kwargs['target_value_code']
        
        # 타겟변수명 조회
        var_map_instance = TbVarMap.objects.get(var_code=target_value_code)
        target_value_name = var_map_instance.var_name
        
        # 모델목록 조회
        model = TbModel.objects.filter(target_code=target_value_code).values()
        model_list = list(model)
        print(model_list)
        
        context = { 'target_value_code' : target_value_code,
                    'target_value_name' : target_value_name,
                    'model_list' : model_list
                   }
        return render(request, 'predict_analytic/predict_analytic.html', context=context)

class SearchOperateNumberView(TemplateView):
    def post(self, request):
        op_num = request.POST.get('op_num')
        print(op_num)
        smart_op_sum = TbSmartopSum.objects.get(op_num=op_num)
        smart_op_sum_dict = model_to_dict(smart_op_sum)
        print(type(smart_op_sum_dict))
        print(smart_op_sum_dict)

        context = {
            'smart_op_sum_dict' : smart_op_sum_dict,
        }
        return HttpResponse(json.dumps(context), content_type="application/json")


class SearchOptimalPredictView(TemplateView):
    def post(self, request):
        target_code = request.POST.get('target_code')
        target_num = request.POST.get('target_num')
        model_info = TbModel.objects.get(target_code=target_code,target_num=target_num)
        model_file_name = model_info.model_file_name   ## 모델 파일명



        #checked_var_list.append(target_value_code)
        smart_op_sum = TbSmartopSum.objects.values()
        smart_op_sum_df = pd.DataFrame(list(smart_op_sum))
        smart_operate_report = SmartOperateReport()
        smart_operate_report.kisco_df = smart_op_sum_df[checked_var_list]


        smart_operate_report = SmartOperateReport()

        clf_from_joblib = joblib.load(model_file_name)

        smart_operate_report.predict_smart_operate(clf_from_joblib)

        smart_operate_report.make_osl_model()
        smart_operate_report.kisco_test_df = smart_operate_report.kisco_df.loc[0].to_frame().T
        # 예측을 하기위해서 사용자가 선택할 데이터들
        input_x_values = ['heavy_scrap_a', 'heavy_scrap_b', 'light_scrap_a', 'light_scrap_b', 'gsa', 'gsb', 'gss', 'mb',
                          'lathe_b']

        smart_operate_report.copy_experience_data(target_value_name=target_code, input_x_values=input_x_values)

        # x_value = 'oxy_bunner'   # 임시로 나중에 영향도높은 순 또는 사용자가 지정한 것 순으로 생성후 탐색
        # smart_operate_report.create_predict_data(model=rr_model,target_value_name=target_value_name,x_value=x_value)
        smart_operate_report.predict_copy_data(model=rr_model, target_value_name=target_code)



        context = {
            'target_code' : target_code,
        }
        return HttpResponse(json.dumps(context), content_type="application/json")



