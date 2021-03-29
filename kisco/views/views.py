from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd

from kisco.models import TbSmartopSum
from kisco.models import TbVarMap

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
        all_var_name = TbVarMap.objects.exclude(var_code = 'op_num').values()

        all_var_name_df = pd.DataFrame(list(all_var_name))
        all_var_name_df.sort_values('seq')



        #all_var_code_list = list(all_var_name_df['var_code'])
        all_var_name_list = list(all_var_name_df['var_name'])
        all_var_code_list = list(all_var_name_df['var_code'])
        var_list = []
        for i in range(len(all_var_code_list)):
            temp = [all_var_code_list[i],all_var_name_list[i]]
            var_list.append(temp)



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



        context = {
            'var_list' : var_list,
            'data_list': data_list,
        }

        #print(smart_op_sum_df)
        #return HttpResponse(json.dumps(context, default=str), content_type="application/json")
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