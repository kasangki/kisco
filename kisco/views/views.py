from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd

from kisco.anaytics.db_util import DBUtil
from kisco.models import TbSmartopSum
from kisco.models import TbVarMap
from kisco.models import TbModel

from django.db import connection



from datetime import datetime
from django.http.response import HttpResponse
import simplejson as json

'''
 * Created by : 강상기
 * Created Date : 2021. 03 .08
 * author 강상기
 * 내용 : 주요데이터분석
 */
'''


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        # 타입코드 
        # steel_out_vol : 출강량
        # power_factor : 역률
        # total_elec_charge : 전력량
        # steel_out_rate : 회수율
        
        target_value_names = ['steel_out_vol', 'power_factor', 'total_elec_charge', 'steel_out_rate']
        target_value_kor_names = ['출강량', '역률', '합계전력량', '회수율']        
        target_value_code = target_value_names[3]
        target_value_name = target_value_kor_names[3]

        #전체변수목록
        all_var_name = TbVarMap.objects.exclude(var_code = 'op_num').values()


        #변수변수목록 Blog.objects.filter(entry__headline__contains='Lennon')
        #all_var_name = TbVarMap.objects.exclude(var_code='op_num' ).values()
        #DataFrame명[DataFrame명['칼럼명'] == 값]

        all_var_name_df = pd.DataFrame(list(all_var_name))
        all_var_name_df.sort_values('seq')

        # 모든변수
        all_var_name_list = list(all_var_name_df['var_name'])
        all_var_code_list = list(all_var_name_df['var_code'])
        var_list = []
        for i in range(len(all_var_code_list)):
            temp = [all_var_code_list[i],all_var_name_list[i]]
            var_list.append(temp)

        db_util = DBUtil()
        ttt_var_list = db_util.get_var_name_list('T',all_var_name_df)   ## 시간변수목록
        steel_var_list = db_util.get_var_name_list('S', all_var_name_df)  ## 고철종류 변수목록
        mat_var_list = db_util.get_var_name_list('M', all_var_name_df)   ## 부자재 변수목록
        equip_var_list = db_util.get_var_name_list('Q', all_var_name_df)  ## 설비변수 목록
        etc_var_list = db_util.get_var_name_list('E', all_var_name_df)   ## 기타 변수 목록



        var_name = 'entry_time'
        target_name = 'steel_out_vol'
        feature_columns  = [var_name,target_name]
        smartTopSum = TbSmartopSum.objects.values()
        smart_top_sum_df = pd.DataFrame(list(smartTopSum))
        data_list = smart_top_sum_df[feature_columns]

        x_list = list(smart_top_sum_df[var_name])
        y_list = list(smart_top_sum_df[target_name])

        data_list = []
        for i in range(len(x_list)):
            temp = [x_list[i],y_list[i]]
            data_list.append(temp)

        ## 모델 목록조회
        model = TbModel.objects.filter(target_code=target_value_code).values()
        model_list = list(model)

        context = {
            'var_list' : var_list,
            'ttt_var_list' : ttt_var_list,
            'steel_var_list' : steel_var_list,
            'mat_var_list': mat_var_list,
            'equip_var_list': equip_var_list,
            'etc_var_list': etc_var_list,
            'data_list': data_list,
            'target_value_code': target_value_code,
            'target_value_name': target_value_name,
            'model_list' : model_list,
        }
       
        return render(request, 'index.html', context=context)


    ## 변수 타입별 변수 목록 조회
    def  get_var_name_list(self,var_type,all_var_name_df):
        # 선택변수 목록
        select_var_name_df = all_var_name_df[all_var_name_df['var_type'] == var_type]

        select_var_name_list = list(select_var_name_df['var_name'])
        select_var_code_list = list(select_var_name_df['var_code'])
        select_var_list = []
        for i in range(len(select_var_code_list)):
            temp = [select_var_code_list[i], select_var_name_list[i]]
            select_var_list.append(temp)
        return select_var_list

    ## 변수 타입별 변수 목록 조회
    def  get_var_name_query_list(self,target_code,target_num, var_type):
        # 선택변수 목록
        query = '''select a.target_code ,
                       a.var_code ,
                       b.var_name
                from  tb_var_info a, tb_var_map b
                where a.target_code = %s
                and a.target_num = %s
                and a.var_code = b.var_code
                and b.var_type = %s '''
        cursor = connection.cursor()
        cursor.execute(query, (target_code, target_num,var_type))
        var_info_list = cursor.fetchall()


        return var_info_list


class IndexMainDataAna(TemplateView) :
    def get(self, request, *args, **kwargs):
        # 타입코드
        # steel_out_vol : 출강량
        # power_factor : 역률
        # total_elec_charge : 합계전력량
        # steel_out_rate : 회수율
        # 
        target_value_names = ['steel_out_vol', 'power_factor', 'total_elec_charge', 'steel_out_rate']
        target_value_kor_names = ['출강량', '역률', '합계전력량', '회수율']


        target_value_code_num = kwargs['target_value_code_num']

        target_value_code = target_value_names[target_value_code_num]
        target_value_name = target_value_kor_names[target_value_code_num]



        print(target_value_name)

        #전체변수목록
        all_var_name = TbVarMap.objects.exclude(var_code = 'op_num').values()


        #변수변수목록 Blog.objects.filter(entry__headline__contains='Lennon')
        #all_var_name = TbVarMap.objects.exclude(var_code='op_num' ).values()
        #DataFrame명[DataFrame명['칼럼명'] == 값]

        all_var_name_df = pd.DataFrame(list(all_var_name))
        all_var_name_df.sort_values('seq')





        # 모든변수
        #all_var_code_list = list(all_var_name_df['var_code'])
        all_var_name_list = list(all_var_name_df['var_name'])
        all_var_code_list = list(all_var_name_df['var_code'])
        var_list = []
        for i in range(len(all_var_code_list)):
            temp = [all_var_code_list[i],all_var_name_list[i]]
            var_list.append(temp)

        # 필수변수 목록
        esstial_var_name_df = all_var_name_df[all_var_name_df['var_type'] == 'E']

        esstial_var_name_list = list(esstial_var_name_df['var_name'])
        esstial_var_code_list = list(esstial_var_name_df['var_code'])
        esstial_var_list = []
        for i in range(len(esstial_var_code_list)):
            temp = [esstial_var_code_list[i],esstial_var_name_list[i]]
            esstial_var_list.append(temp)


        # 선택변수 목록
        select_var_name_df = all_var_name_df[all_var_name_df['var_type'] != 'E']

        select_var_name_list = list(select_var_name_df['var_name'])
        select_var_code_list = list(select_var_name_df['var_code'])
        select_var_list = []
        for i in range(len(select_var_code_list)):
            temp = [select_var_code_list[i],select_var_name_list[i]]
            select_var_list.append(temp)





        var_name = 'entry_time'
        #target_code = 'steel_out_vol'
        feature_columns  = [var_name,target_value_code]
        smartTopSum = TbSmartopSum.objects.values()
        smart_top_sum_df = pd.DataFrame(list(smartTopSum))
        data_list = smart_top_sum_df[feature_columns]

        x_list = list(smart_top_sum_df[var_name])
        y_list = list(smart_top_sum_df[target_value_code])

        data_list = []
        for i in range(len(x_list)):
            temp = [x_list[i],y_list[i]]
            data_list.append(temp)


        model = TbModel.objects.filter(target_code=target_value_code).values()
        model_list = list(model)



        context = {
            'var_list' : var_list,
            'esstial_var_list' : esstial_var_list,
            'select_var_list' : select_var_list,
            'data_list': data_list,
            'target_value_code' : target_value_code,
            'target_value_name' : target_value_name,
            'model_list' : model_list
        }

        return render(request, 'index.html', context=context)



class PredictAnalyticView(TemplateView) :
    def get(self, request, *args, **kwargs):



        target_value_code_num = kwargs['target_value_code_num']


        return render(request, 'index.html', context=context)

class Index2View(TemplateView):
    def get(self, request, *args, **kwargs):

        smart_op_sum_list = TbSmartopSum.objects.order_by('op_num')
        #smart_op_sum_df = pd.DataFrame(list(smart_op_sum))
        context = {
            'smart_op_sum_list' : smart_op_sum_list
        }
        #print(smart_op_sum_df)
        #return HttpResponse(json.dumps(context, default=str), content_type="application/json")
        return render(request, 'index2.html', context=context)