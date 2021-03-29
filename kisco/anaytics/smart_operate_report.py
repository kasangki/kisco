import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


class SmartOperateReport():
    def __init__(self):
        #file_name = './data/smart_operate.csv'
        #file_name_test = './data/smart_operate_test.csv'
        self.kisco_df = ''
        self.kisco_df_test_df = ''
        self.x_value_dict = {}
        self.target_value_name = ''
        #print(self.hanchul_df.columns)
        # self.x_value = ['중량A', '중량B', '경량A', '경량B', 'GSA', 'GSB', 'GSS', 'MB', '선반설B', '출강량']
        # self.target_value_name = '출강량'
        #
        # self.x_value_dict = {'출강량_01': x_value}
        # self.case = '출강량_01'

    def set_values(self,x_values,target_value_name,case):
        self.x_value_dict[case] = x_values
        self.target_value_name = target_value_name


    ''' RandomForestRegressor 학습 '''
    def train_smart_operate(self):
        # 데이터 불러오기

        feature_columns = list(self.kisco_df.columns.difference([self.target_value_name]))
        X = self.kisco_df[feature_columns]
        y = self.kisco_df[self.target_value_name]

        train_x, test_x, train_y, test_y = train_test_split(X, y, train_size=0.7, test_size=0.3)
        # print(train_x.shape, test_x.shape, train_y.shape, test_y.shape)
        # print(feature_columns)
        # print(y.describe())

        ## RandomForestRegressor 알고리즘 적용
        model = RandomForestRegressor(n_estimators=100, max_depth=100)

        # RandomForestRegressor 학습시작
        model.fit(train_x, train_y)

        return model, train_x

    def train_smart(self,target_value_name):
        smart_operate_report = SmartOperateReport()
        x_values = ['중량A', '중량B', '경량A', '경량B', 'GSA', 'GSB', 'GSS', 'MB', '선반설B', '출강량']
        target_value_name = '출강량'
        case = '출강량_01'
        smart_operate_report.set_values(x_values=x_values, target_value_name=target_value_name, case=case)

        rr_model, rr_x_train = smart_operate_report.train_smart_operate()
        print('변수중요도 =====>>>>>', rr_model.feature_importances_)
        rr_feat_importances = pd.Series(rr_model.feature_importances_, index=rr_x_train.columns)
        print(rr_feat_importances)


