
'''
 * Created by : 강상기
 * Created Date : 2021. 3 .10
 * author 강상기
 * 내용 : 주요데이터분석 - 싱글변수
 */
'''

from django.shortcuts import render
from django.views.generic import TemplateView
from kisco.models import TbSmartopSum, TbVarMap,TbTargetValue
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



## 모델 생성하기
class TrainModelViews(TemplateView):
    # 모델 생성하기
    def make_model(request):
        checked_var_list = request.POST.getlist('checkedVarList[]')
        # tb_var_info 테이블에 데이터를 넣기 위해서
        var_info_list = checked_var_list.copy()
        target_value_code = request.POST.getlist('target_value_code')[0]
        target_value_names = ['steel_out_vol', 'total_elec_charge', 'power_factor', 'steel_out_rate']
        target_value_kor_names = ['출강량', '합계전력량', '역률', '회수율']
        alg_names = ['RandomForrest']
        print(checked_var_list)
        ''' 타겟 변수'''
        #target_value_name = 'steel_out_rate'
        #target_value_names = ['steel_out_vol', 'power_factor', 'total_elec_charge', 'steel_out_rate']

        #feature_columns = [var_name, 'steel_out_vol', 'power_factor', 'total_elec_charge', 'steel_out_rate']
        checked_var_list.append(target_value_code)
        smart_op_sum = TbSmartopSum.objects.values()
        smart_op_sum_df = pd.DataFrame(list(smart_op_sum))
        smart_operate_report = SmartOperateReport()
        smart_operate_report.kisco_df = smart_op_sum_df[checked_var_list]
        ''' 테스트용 데이터'''



        case = '출강량_01'
        smart_operate_report.set_values(x_values=checked_var_list, target_value_name=target_value_code, case=case)

        rr_model, rr_x_train = smart_operate_report.train_smart_operate()



        model = TbModel.objects.filter(target_code=target_value_code).values()
        model_df = pd.DataFrame(list(model))
        print("모델 데이터프레임 ===> ",model_df.empty)
        if( model_df.empty) :
            target_num = 1
        else :
            target_num = model_df['target_num'].max() + 1

        create_dtm = datetime.now()
        update_dtm = datetime.now()
        target_value_kor_name = TbVarMap.objects.filter(var_code=target_value_code).first().var_name

        model_name = target_value_kor_name + '_' + str(target_num)
        model_file_name = './static/model/' + target_value_code + '_' + str(target_num) + '.pkl'



        ## 모델 테이블에 모델 저장
        model_instance = TbModel(target_code=target_value_code, target_num=target_num,model_name=model_name, accuracy='99.99',
                                 alg_name=alg_names[0],
                                 create_dtm=create_dtm, update_dtm=create_dtm, model_file_name=model_file_name)

        model_instance.save(force_insert=True)

        ## 변수정보 테이블에 변수목록 저장
        for var_code in var_info_list :
            #var_map_instance = TbVarMap.objects.get(var_code=var_code)
            var_info_model = TbVarInfo(target_code=target_value_code,target_num=model_instance.target_num,var_code=var_code)
            var_info_model.save(force_insert=True)

        
        ##  생성된 모델 저장
        joblib.dump(rr_model,model_file_name)
        print('변수중요도 =====>>>>>', rr_model.feature_importances_)

        ## 모델 목록조회( datatime 에러남)
        # model = TbModel.objects.filter(target_code=target_value_code).values()
        # model_list = list(model)

        query = '''select target_code ,
               target_num ,
               model_file_name,
               model_name ,
               accuracy ,
               alg_name ,
               to_char(create_dtm, %s) as create_dtm,
               to_char(update_dtm, %s) as update_dtm
        from tb_model 
        where target_code = %s'''
        cursor = connection.cursor()
        cursor.execute(query, ('YYYY-MM-DD HH:MI:SS','YYYY-MM-DD HH:MI:SS',target_value_code))
        model_list = cursor.fetchall()

        target_value = TbTargetValue.objects.get(target_value_code=target_value_code)
        target_value_code_num = target_value.pk

        context = {
            'checked_var_list' : checked_var_list,
            'model_list' : model_list,
            'target_value_code_num' : target_value_code_num,
        }

        return HttpResponse(json.dumps(context), content_type="application/json")
    

## 모델 생성하기
class TrainPredictModelViews(TemplateView):
    # 모델 생성하기
    def make_predict_model(request):

        checked_var_list = request.POST.getlist('checkedVarList[]')
        # tb_var_info 테이블에 데이터를 넣기 위해서
        var_info_list = checked_var_list.copy()
        target_value_code = request.POST.getlist('target_value_code')[0]
        target_value_names = ['steel_out_vol',  'total_elec_charge', 'power_factor', 'steel_out_rate']
        target_value_kor_names = ['출강량', '합계전력량', '역률',  '회수율']
        alg_names = ['RandomForrest']
        print(checked_var_list)
        ''' 타겟 변수'''
        #target_value_name = 'steel_out_rate'
        #target_value_names = ['steel_out_vol', 'power_factor', 'total_elec_charge', 'steel_out_rate']

        #feature_columns = [var_name, 'steel_out_vol', 'power_factor', 'total_elec_charge', 'steel_out_rate']
        checked_var_list.append(target_value_code)
        smart_op_sum = TbSmartopSum.objects.values()
        smart_op_sum_df = pd.DataFrame(list(smart_op_sum))
        smart_operate_report = SmartOperateReport()
        smart_operate_report.kisco_df = smart_op_sum_df[checked_var_list]
        ''' 테스트용 데이터'''

        print(smart_op_sum_df)

        case = '출강량_01'
        smart_operate_report.set_values(x_values=checked_var_list, target_value_name=target_value_code, case=case)

        rr_model, rr_x_train = smart_operate_report.train_smart_operate()



        model = TbModel.objects.filter(target_code=target_value_code).values()
        model_df = pd.DataFrame(list(model))
        print("모델 데이터프레임 ===> ",model_df.empty)
        if( model_df.empty) :
            target_num = 1
        else :
            target_num = model_df['target_num'].max() + 1

        create_dtm = datetime.now()
        target_value_kor_name = TbVarMap.objects.filter(var_code=target_value_code).first().var_name

        model_name = target_value_kor_name + '_' + str(target_num)
        model_file_name = './static/model/' + target_value_code + '_' + str(target_num) + '.pkl'




        model_instance = TbModel(target_code=target_value_code, target_num=target_num,model_name=model_name, accuracy='99.99',
                                 alg_name=alg_names[0],
                                 create_dtm=create_dtm, update_dtm=create_dtm, model_file_name=model_file_name)

        model_instance.save(force_insert=True)


        for var_code in var_info_list :
            #var_map_instance = TbVarMap.objects.get(var_code=var_code)
            var_info_model = TbVarInfo(target_code=target_value_code,target_num=model_instance.target_num,var_code=var_code)
            var_info_model.save(force_insert=True)


        joblib.dump(rr_model,model_file_name)
        print('변수중요도 =====>>>>>', rr_model.feature_importances_)

        rr_feat_importances = pd.Series(rr_model.feature_importances_, index=rr_x_train.columns)
        print(rr_feat_importances)

        smart_operate_report.kisco_test_df = smart_operate_report.kisco_df.loc[0]

        clf_from_joblib = joblib.load(model_file_name)
        smart_operate_report.predict_smart_operate(clf_from_joblib)

        smart_operate_report.make_osl_model()
        smart_operate_report.kisco_test_df = smart_operate_report.kisco_df.loc[0].to_frame().T
        # 예측을 하기위해서 사용자가 선택할 데이터들
        input_x_values = ['heavy_scrap_a','heavy_scrap_b','light_scrap_a','light_scrap_b','gsa','gsb','gss','mb','lathe_b']

        smart_operate_report.copy_experience_data(target_value_name=target_value_code,input_x_values=input_x_values)

        # x_value = 'oxy_bunner'   # 임시로 나중에 영향도높은 순 또는 사용자가 지정한 것 순으로 생성후 탐색
        # smart_operate_report.create_predict_data(model=rr_model,target_value_name=target_value_name,x_value=x_value)
        smart_operate_report.predict_copy_data(model=rr_model,target_value_name=target_value_code)

        context = {
            'checked_var_list' : checked_var_list,
        }


        return HttpResponse(json.dumps(context), content_type="application/json")




# 생성된 모델 예측
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

# 최적추천탐색
class SearchOptimalPredictView(TemplateView):
    def post(self, request, *args, **kwargs):
        target_code = request.POST.get('target_code')
        target_num = request.POST.get('target_num')
        #checked_global_list = request.POST.getlist('checkedGlobalList[]')
        var_list = request.POST.getlist('var_list[]')   # 변수목록
        var_name_list = request.POST.getlist('var_name_list[]')   # 변수명 리스트


        # test_df = pd.Series(var_list,index=var_name_list).to_frame().T



        # for i in range(len(var_list)):
        #     temp = [var_list[i],var_list[i]]
        #     print(temp)

        print(var_list)
        print(var_name_list)

        # 모델 정보에 해당되는 변수 목록 조회
        var_info = TbVarInfo.objects.filter(target_code=target_code, target_num=target_num).values()
        var_info_list = list(var_info)
        var_info_list = pd.DataFrame(list(var_info_list))['var_code'].tolist()



        # 모델 정보 조회
        model_info = TbModel.objects.get(target_code=target_code,target_num=target_num)
        model_file_name = model_info.model_file_name   ## 모델 파일명



        # 메인데이터에서 예측할 데이터 추출
        smart_op_sum = TbSmartopSum.objects.values()
        smart_op_sum_df = pd.DataFrame(list(smart_op_sum))
        smart_operate_report = SmartOperateReport()
        smart_operate_report.kisco_source_df = smart_op_sum_df


        smart_operate_report.kisco_test_df = pd.Series(var_list,index=var_name_list).to_frame().T.astype(float)
        var_info_list.append(target_code)
        smart_operate_report.kisco_df = smart_op_sum_df[var_info_list]



        clf_from_joblib = joblib.load(model_file_name)

        #smart_operate_report.predict_smart_operate(clf_from_joblib)

        #smart_operate_report.make_osl_model()


        # 예측을 하기위해서 사용자가 선택할 데이터들
        # input_x_values = ['heavy_scrap_a', 'heavy_scrap_b', 'light_scrap_a', 'light_scrap_b', 'gsa', 'gsb', 'gss', 'mb',
        #                   'lathe_b']

        input_x_values = var_name_list

        smart_operate_report.copy_experience_data(target_value_name=target_code, input_x_values=input_x_values)

        # x_value = 'oxy_bunner'   # 임시로 나중에 영향도높은 순 또는 사용자가 지정한 것 순으로 생성후 탐색
        # smart_operate_report.create_predict_data(model=rr_model,target_value_name=target_value_name,x_value=x_value)
        smart_operate_report.predict_copy_data(model=clf_from_joblib, target_value_name=target_code)

        for i in range(len(var_name_list)) :
            smart_operate_report.y_final_result_sr[var_name_list[i]] = float(var_list[i])
        print("최종결과 ==== > ",smart_operate_report.y_final_result_sr[0])
        # 최종 결과값 문자열로 변환
        y_final_result_dict = smart_operate_report.y_final_result_sr.to_dict()
        for key,value in y_final_result_dict.items():
            y_final_result_dict[key] = str(value)


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
        ttt_var_list = db_util.set_y_final_value_list('T', all_var_name_df,y_final_result_dict,var_name_list)  ## 시간변수목록
        steel_var_list = db_util.set_y_final_value_list('S', all_var_name_df,y_final_result_dict,var_name_list)  ## 고철종류 변수목록
        mat_var_list = db_util.set_y_final_value_list('M', all_var_name_df,y_final_result_dict,var_name_list)  ## 부자재 변수목록
        equip_var_list = db_util.set_y_final_value_list('Q', all_var_name_df,y_final_result_dict,var_name_list)  ## 설비변수 목록
        etc_var_list = db_util.set_y_final_value_list('E', all_var_name_df,y_final_result_dict,var_name_list)  ## 기타 변수 목록



        #smart_operate_report.y_final_result_sr = repr(smart_operate_report.y_final_result_sr)
        context = {
            'target_code' : target_code,
            'final_result' : y_final_result_dict,
            'ttt_var_list' : ttt_var_list,
            'steel_var_list' : steel_var_list,
            'mat_var_list': mat_var_list,
            'equip_var_list': equip_var_list,
            'etc_var_list': etc_var_list,

        }
        return HttpResponse(json.dumps(context), content_type="application/json")




# 모델에 해당되는 변수 목록 조회
class SearchVarInfoView(TemplateView):
    def post(self, request, *args, **kwargs):
        target_code = request.POST.get('target_code')
        target_num = request.POST.get('target_num')
        # var_info = TbVarInfo.objects.filter(target_code=target_code, target_num=target_num).values()
        # var_info_list = list(var_info)

        query = '''select a.target_code as target_code ,
                   a.target_num as target_num ,                   
                   a.var_code as var_code  ,
                   b.var_name as var_name
            from tb_var_info a, tb_var_map b
            where a.var_code = b.var_code
            and a.target_code = %s
            and a.target_num = %s'''
        cursor = connection.cursor()
        cursor.execute(query,(target_code,target_num))
        var_info_list = cursor.fetchall()
        # var_info_df = pd.DataFrame(datas, columns=['target_code', 'target_num', 'var_code','var_name']).tolist()
        # print(var_info_df)

        # 전체변수목록
        all_var_name = TbVarMap.objects.exclude(var_code='op_num').values()
        all_var_name_df = pd.DataFrame(list(all_var_name))
        all_var_name_df.sort_values('seq')

        index_view = IndexView()
        mat_var_list = index_view.get_var_name_query_list(target_code, target_num, 'M')  ## 부자재 변수목록
        equip_var_list = index_view.get_var_name_query_list(target_code, target_num, 'Q')  ## 설비변수 목록
        etc_var_list = index_view.get_var_name_query_list(target_code, target_num, 'E')  ## 기타 변수 목록

        ttt_var_list = index_view.get_var_name_query_list(target_code,target_num,'T')  ## 시간변수목록
        steel_var_list = index_view.get_var_name_query_list(target_code,target_num,'S')  ## 고철종류 변수목록


        print(mat_var_list)
        context = {
            'var_info_list' : var_info_list,
            'ttt_var_list': ttt_var_list,
            'steel_var_list': steel_var_list,
            'mat_var_list': mat_var_list,
            'equip_var_list': equip_var_list,
            'etc_var_list': etc_var_list,
        }
        return HttpResponse(json.dumps(context), content_type="application/json")







