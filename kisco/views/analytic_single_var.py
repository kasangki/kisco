
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


from kisco.anaytics.smart_operate_report import SmartOperateReport
from kisco.anaytics.quantile_analytics import QuantileAnalytics

class AnalyticSingleVarView(TemplateView):
    def power_factor(request):
        context = {}
        return render(request, 'main_data/power_factor.html', context=context)



    def analytic_single_var(request):
        var_name = request.GET.get('var_name')


        quantile_feature_columns  = [var_name,'power_factor']
        quantile_sum = TbSmartopSum.objects.values()
        quantile_sum_df = pd.DataFrame(list(quantile_sum))
        quantile_sum_df = quantile_sum_df[quantile_feature_columns]


        # 사분위수 분석을 위한 데이터
        quantile_analytics = QuantileAnalytics()
        quantile_target_name = 'power_factor'
        quantile_analytics.get_quantile_analytics(var_name,quantile_target_name,quantile_sum_df)
        quantile_img_list = quantile_analytics.quantile_img_list
        quantile_title_list = quantile_analytics.quantile_title_list
        print(quantile_img_list);
        ## 사분위수 처리 끝

        context = {
            'title_list': quantile_title_list,
            'img_list': quantile_img_list,
            'quantile_title_list': quantile_title_list,
            'quantile_img_list': quantile_img_list
            # 'y_list': y_list,
            # 'data_list' : data_list,
            # 'result_list': result_list

        }

        return HttpResponse(json.dumps(context), content_type="application/json")




        target_name = 'steel_out_vol'
        target_value_names = ['steel_out_vol', 'power_factor', 'total_elec_charge', 'steel_out_rate']

        feature_columns = [var_name, 'steel_out_vol', 'power_factor', 'total_elec_charge', 'steel_out_rate']
        smart_top_sum = TbSmartopSum.objects.values()
        smart_top_sum_df = pd.DataFrame(list(smart_top_sum))
        smart_top_sum_df = smart_top_sum_df[feature_columns]

        if(var_name == 'entry_time') :
            cond = smart_top_sum_df['entry_time'] <= 5
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['entry_time'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'melt_start_time') :
            cond = smart_top_sum_df['melt_start_time'] <=22
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['melt_start_time'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'melt_add_time') :
            cond = smart_top_sum_df['melt_add_time'] <= 16
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['melt_add_time'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'refine_time') :
            cond = smart_top_sum_df['refine_time'] <= 17
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['refine_time'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'steel_out_time') :
            cond = smart_top_sum_df['steel_out_time'] <= 7
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['steel_out_time'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'total_time') :
            cond = smart_top_sum_df['total_time'] <= 55
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['total_time'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'heavy_scrap_a') :
            cond = smart_top_sum_df['heavy_scrap_a'] <= 60
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['heavy_scrap_a'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'heavy_scrap_b') :
            cond = smart_top_sum_df['heavy_scrap_b'] <= 60
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['heavy_scrap_b'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'light_scrap_a') :
            cond = smart_top_sum_df['light_scrap_a'] <= 85
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['light_scrap_a'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'light_scrap_b') :
            cond = smart_top_sum_df['light_scrap_b'] <= 15
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['light_scrap_b'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'gsa') :
            cond = smart_top_sum_df['gsa'] <= 30
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['gsa'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'gsb') :
            cond = smart_top_sum_df['gsb'] <= 5
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['gsb'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'gss') :
            cond = smart_top_sum_df['gss'] <= 4
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['gss'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'mb') :
            cond = smart_top_sum_df['mb'] <= 5
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['mb'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]
        if(var_name == 'lathe_b') :
            cond = smart_top_sum_df['lathe_b'] <= 40
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['lathe_b'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'scrap_metal_usage') :
            cond = smart_top_sum_df['scrap_metal_usage'] <= 130
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['scrap_metal_usage'] > 100
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'scrap_avg_ton') :
            cond = smart_top_sum_df['scrap_avg_ton'] <= 10
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['scrap_avg_ton'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'gravity') :
            cond = smart_top_sum_df['gravity'] <= 0.85
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['gravity'] > 0.4
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'briquet_hp') :
            cond = smart_top_sum_df['briquet_hp'] <= 1000
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['briquet_hp'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'briquet_hp') :
            cond = smart_top_sum_df['briquet_hp'] <= 1000
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['briquet_hp'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]


        if(var_name == 'bri_hp2') :
            cond = smart_top_sum_df['bri_hp2'] <= 1000
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['bri_hp2'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]


        if(var_name == 'elec_fumace_volt') :
            cond = smart_top_sum_df['elec_fumace_volt'] <= 1000
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['elec_fumace_volt'] > 450
            smart_top_sum_df = smart_top_sum_df[cond]


        if(var_name == 'elec_fumace_current') :
            cond = smart_top_sum_df['elec_fumace_current'] <= 1000
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['elec_fumace_current'] > 100
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'gsk') :
            cond = smart_top_sum_df['gsk'] <= 1000
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['gsk'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'oxy_bunner') :
            cond = smart_top_sum_df['oxy_bunner'] <= 1100
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['oxy_bunner'] > 500
            smart_top_sum_df = smart_top_sum_df[cond]


        if(var_name == 'oxy_lance') :
            cond = smart_top_sum_df['oxy_lance'] <= 1750
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['oxy_lance'] > 500
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'lance_flux') :
            cond = smart_top_sum_df['lance_flux'] <= 3000
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['lance_flux'] > 900
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'lance_height') :
            cond = smart_top_sum_df['lance_height'] <= 1400
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['lance_height'] > 800
            smart_top_sum_df = smart_top_sum_df[cond]


        if(var_name == 'lance_width') :
            cond = smart_top_sum_df['lance_width'] <= 1600
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['lance_width'] > 500
            smart_top_sum_df = smart_top_sum_df[cond]


        if(var_name == 'lance_til_area') :
            # cond = smart_top_sum_df['lance_til_area'] <= 10
            # smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['lance_til_area'] > 0
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'elec_pre_air_vol') :
            cond = smart_top_sum_df['elec_pre_air_vol'] <= 100000
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['elec_pre_air_vol'] > 50000
            smart_top_sum_df = smart_top_sum_df[cond]


        if(var_name == 'master_pos') :
            cond = smart_top_sum_df['master_pos'] <= 6500
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['master_pos'] > 4000
            smart_top_sum_df = smart_top_sum_df[cond]

        if(var_name == 'master_move_distance') :
            cond = smart_top_sum_df['master_move_distance'] <= 2000
            smart_top_sum_df = smart_top_sum_df[cond]
            cond = smart_top_sum_df['master_move_distance'] > 800
            smart_top_sum_df = smart_top_sum_df[cond]


        var_map = TbVarMap.objects.values()
        var_map_df = pd.DataFrame(list(var_map))
        var_map_df = var_map_df.set_index('var_code')



        plt.rc('font', family='Malgun Gothic')
        plt.rcParams["figure.figsize"] = (5.2, 4)
        title_list = []
        img_list = []
        for target_value_name in target_value_names :
            var_x_name = var_map_df.loc[var_name].loc['var_name']
            var_y_name = var_map_df.loc[target_value_name].loc['var_name']

            ana_feature_columns = [var_name, target_value_name]
            ana_df = smart_top_sum_df[ana_feature_columns]
            osl_df = sm.add_constant(ana_df, has_constant='add')
            '''target 변수 제외한 컬럼들을 독립변수로 선택'''
            ana_feature_columns = list(osl_df.columns.difference([target_value_name]))
            X = osl_df[ana_feature_columns]
            y = osl_df[target_value_name]
            train_x, test_x, train_y, test_y = train_test_split(X, y, train_size=0.7, test_size=0.3)

            # Train the MLR / 회귀모델적합
            model = sm.OLS(train_y, train_x)
            fitted_full_model = model.fit()
            coef = fitted_full_model.params[var_name]
            const = fitted_full_model.params['const']

            x_list = list(smart_top_sum_df[var_name])
            y_list = list(smart_top_sum_df[target_value_name])


            #self.save_fig(x_list,y_list,var_name,target_value_name,coef,const)

            #for i in range(len(x_list)):
            for i in range(1000):
                plt.plot(x_list[i], y_list[i], '.', color='blue')
                y = x_list[i]*coef + const
                plt.plot(x_list[i], y, '.', color='red')

            plt.ylabel(var_y_name, size=10)
            plt.xlabel(var_x_name, size=10)
            img_name = './static/img/'+var_name+ '_'+target_value_name+'.png'
            img_list.append(img_name)

            plt.savefig(img_name)
            plt.cla()
            plt.rc('font', family='Malgun Gothic')
            plt.rcParams["figure.figsize"] = (5.2, 4)
            title = [var_x_name,var_y_name,round(coef,4),const]
            title_list.append(title)




        # data_list = []
        # result_list = []
        # for i in range(len(x_list)):
        #     temp = [x_list[i],y_list[i]]
        #     temp_reslut = [x_list[i], yy_list[i]]
        #     data_list.append(temp)
        #     result_list.append(temp_reslut)
        # data_list = data_list[:300]
        # result_list = result_list[:300]



        context = {
           'title_list': title_list,
           'img_list' : img_list ,
           'quantile_title_list' : quantile_title_list,
           'quantile_img_list' : quantile_img_list
           # 'y_list': y_list,
           # 'data_list' : data_list,
           # 'result_list': result_list

        }


        return HttpResponse(json.dumps(context), content_type="application/json")
        #return render(request, 'index.html', context=context)

    # def select_valuable(self):
    #     osl_df = sm.add_constant(self.hanchul_df, has_constant='add')
    #     '''target 변수 제외한 컬럼들을 독립변수로 선택'''
    #     feature_columns = list(osl_df.columns.difference([self.target_value_name]))
    #
    #     X = osl_df[feature_columns]
    #     y = osl_df[self.target_value_name]
    #     train_x, test_x, train_y, test_y = train_test_split(X, y, train_size=0.7, test_size=0.3)
    #
    #     # Train the MLR / 회귀모델적합
    #     model = sm.OLS(train_y, train_x)
    #     self.fitted_full_model = model.fit()





    # 모델 생성하기
    def make_model(request):
        checked_var_list = request.POST.getlist('checkedVarList[]')
        # tb_var_info 테이블에 데이터를 넣기 위해서
        var_info_list = checked_var_list.copy()
        target_value_code = request.POST.getlist('target_value_code')[0]
        target_value_names = ['steel_out_vol', 'power_factor', 'total_elec_charge', 'steel_out_rate']
        target_value_kor_names = ['출강량', '역률', '합계전력량', '회수율']
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
        update_dtm = datetime.now()
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