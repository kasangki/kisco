from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import simplejson as json

from django.shortcuts import render ,redirect


from django.db import connection



# Create your views here.
def report(request):
    print('보고서첫페이지')
    return render(request, 'report.html')


def search_report(request):
    print('보고서 검색')
    report_start_date = request.POST.get('report_start_date', None)
    report_end_date = request.POST.get('report_end_date', None)
    target_code = request.POST.get('target_code', None)
    day_query = '''
                select to_char(create_dtm,'YYYY-MM-DD')
                     , round(sum('''+ target_code + ''')) 
                from tb_smartop_sum_report
                where create_dtm>=%s and create_dtm <= %s
                group by to_char(create_dtm, 'YYYY-MM-DD')
                order by to_char(create_dtm, 'YYYY-MM-DD');
     '''

    cursor = connection.cursor()
    cursor.execute(day_query, (report_start_date, report_end_date))
    day_data_list = cursor.fetchall()
    print(day_data_list)

    month_query = '''
               select to_char(create_dtm,'YYYY-MM')
                     , round(sum(''' + target_code + ''')) 
                From tb_smartop_sum_report
                where create_dtm>='2020-01-01' and create_dtm <= '2021-01-01'
                group by to_char(create_dtm, 'YYYY-MM')
                order by to_char(create_dtm, 'YYYY-MM')
                '''

    cursor = connection.cursor()
    cursor.execute(month_query, (report_start_date, report_end_date))
    month_data_list = cursor.fetchall()
    print(month_data_list)
    context = {
        'day_data_list' : day_data_list,
        'month_data_list' : month_data_list,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

def dashboard(request):
    print('보고서 검색')
    # report_start_date = request.POST.get('report_start_date', None)
    # report_end_date = request.POST.get('report_end_date', None)
    report_start_date = '2020-01-01'
    report_end_date = '2021-02-28'
    target_code = 'steel_out_vol'
    day_query = '''
                select to_char(create_dtm,'YYYY-MM-DD')
                     , round(sum('''+ target_code + ''')) 
                from tb_smartop_sum_report
                where create_dtm>=%s and create_dtm <= %s
                group by to_char(create_dtm, 'YYYY-MM-DD')
                order by to_char(create_dtm, 'YYYY-MM-DD');
     '''

    cursor = connection.cursor()
    cursor.execute(day_query,(report_start_date, report_end_date))
    day_data_list = cursor.fetchall()
    print(day_data_list)

    month_query = '''
               select to_char(create_dtm,'YYYY-MM')
                     , round(sum(''' + target_code + ''')) 
                From tb_smartop_sum_report
                where create_dtm>=%s and create_dtm <= %s
                group by to_char(create_dtm, 'YYYY-MM')
                order by to_char(create_dtm, 'YYYY-MM')
                '''

    cursor = connection.cursor()
    cursor.execute(month_query, (report_start_date, report_end_date))
    month_data_list = cursor.fetchall()
    print(month_data_list)
    context = {
        'day_data_list' : day_data_list,
        'month_data_list' : month_data_list,
    }
    return render(request, 'dashboard.html', context=context)

# Create your views here.
