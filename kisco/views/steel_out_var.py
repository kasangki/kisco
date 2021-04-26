
'''
 * Created by : 강상기
 * Created Date : 2021. 3 .10
 * author 강상기
 * 내용 : 주요데이터분석 - 출강량
 */
'''

from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd




class SteelOutVarView(TemplateView):
    def get(self, request, *args, **kwargs):
        type_code = request.GET.get('type_code')
        print(type_code)
        var_map_list = []
        context = {
            'var_map_list': var_map_list,
        }

        return render(request, 'main_data/steel_out_var.html', context=context)
