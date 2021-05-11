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


class QuantileAnalytics():
    def __init__(self):
        self.quantile_title_list = []
        self.quantile_img_list = []
        self.quantile_target_name = ''
        self.var_name = ''

    def get_quantile_analytics(self,var_name,quantile_target_name,smart_top_sum_df):
        self.var_name = var_name
        self.quantile_target_name = quantile_target_name
        ten = smart_top_sum_df[var_name].quantile(q=0.1,interpolation='nearest')
        nineteen = smart_top_sum_df[var_name].quantile(q=0.9, interpolation='nearest')

        # 사분위수 분석을 위한 데이터
        desc = smart_top_sum_df.describe()
        mean = desc.values[1][0]
        std = desc.values[2][0]
        min = desc.values[3][0]
        first_quantile = desc.values[4][0]
        second_quantile = desc.values[5][0]
        third_quantile = desc.values[6][0]
        max = desc.values[7][0]
        
        first_quantile = ten # 10프로 이하
        third_quantile = nineteen # 90프로 이상

        first_quantile_conf = smart_top_sum_df[var_name] <= first_quantile
        mid_start_quantile_conf = smart_top_sum_df[var_name] > first_quantile
        mid_last_quantile_conf = smart_top_sum_df[var_name] < third_quantile
        third_quantile_conf = smart_top_sum_df[var_name] >= third_quantile

        first_quantile_df = smart_top_sum_df[first_quantile_conf]
        mid_quantile_df = smart_top_sum_df[mid_start_quantile_conf & mid_last_quantile_conf]
        third_quantile_df = smart_top_sum_df[third_quantile_conf]

        print(first_quantile_df)
        print(mid_quantile_df)
        print(third_quantile_df)
        print(smart_top_sum_df)

        var_map = TbVarMap.objects.values()
        var_map_df = pd.DataFrame(list(var_map))
        var_map_df = var_map_df.set_index('var_code')




        self.var_x_name = var_map_df.loc[var_name].loc['var_name']
        self.var_y_name = var_map_df.loc[quantile_target_name].loc['var_name']

        ana_feature_columns = [self.var_name, quantile_target_name]

        quantile_symbol = '10이하'
        self.start_ana(first_quantile_df[ana_feature_columns],quantile_symbol)  # 25% 이내
        quantile_symbol = '75이하'
        self.start_ana(mid_quantile_df[ana_feature_columns],quantile_symbol)   # 25%에서 75% 이내 
        quantile_symbol = '90이상'
        self.start_ana(third_quantile_df[ana_feature_columns],quantile_symbol) # 75# 이상
        quantile_symbol = '전체'
        self.start_ana(smart_top_sum_df[ana_feature_columns],quantile_symbol)  # 전체






    def start_ana(self,ana_df,quantile_symbol):
        plt.rc('font', family='Malgun Gothic')
        plt.rcParams["figure.figsize"] = (5.2, 4)

        osl_df = sm.add_constant(ana_df, has_constant='add')
        '''target 변수 제외한 컬럼들을 독립변수로 선택'''
        ana_feature_columns = list(osl_df.columns.difference([self.quantile_target_name]))
        X = osl_df[ana_feature_columns]
        y = osl_df[self.quantile_target_name]
        train_x, test_x, train_y, test_y = train_test_split(X, y, train_size=0.7, test_size=0.3)

        # Train the MLR / 회귀모델적합
        model = sm.OLS(train_y, train_x)
        fitted_full_model = model.fit()
        coef = fitted_full_model.params[self.var_name]
        const = fitted_full_model.params['const']

        x_list = list(ana_df[self.var_name])
        y_list = list(ana_df[self.quantile_target_name])

        # self.save_fig(x_list,y_list,var_name,target_value_name,coef,const)

        # for i in range(len(x_list)):
        for i in range(400):
            plt.plot(x_list[i], y_list[i], '.', color='blue')
            y = x_list[i] * coef + const
            plt.plot(x_list[i], y, '.', color='red')

        plt.ylabel(self.var_y_name, size=10)
        plt.xlabel(self.var_x_name, size=10)
        img_name = './static/img/' + self.var_name + '_' + self.quantile_target_name + '_'+quantile_symbol+'.png'


        plt.savefig(img_name)
        plt.cla()
        plt.rc('font', family='Malgun Gothic')
        plt.rcParams["figure.figsize"] = (5.2, 4)
        title = [self.var_x_name, self.var_y_name, round(coef, 4), const, quantile_symbol]
        print(title)
        print(img_name)
        self.quantile_img_list.append(img_name)
        self.quantile_title_list.append(title)
