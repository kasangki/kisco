from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd

from kisco.models import TbSmartopSum

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

        smart_op_sum_list = TbSmartopSum.objects.order_by('op_num')
        #smart_op_sum_df = pd.DataFrame(list(smart_op_sum))
        context = {
            'smart_op_sum_list' : smart_op_sum_list
        }
        #print(smart_op_sum_df)
        #return HttpResponse(json.dumps(context, default=str), content_type="application/json")
        return render(request, 'index.html', context=context)

