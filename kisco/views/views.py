from django.shortcuts import render
from django.views.generic import TemplateView


'''
 * Created by : 강상기
 * Created Date : 2021. 03 .08
 * author 강상기
 * 내용 : 메인화면
 */
'''


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):

        return render(request, 'index.html')

