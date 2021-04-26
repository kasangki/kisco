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
        self.kisco_test_df = ''
        self.experience_search_df = ''
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

    ''' RandomForestRegressor 예측 '''
    def predict_smart_operate(self, model):
        feature_columns = list(self.kisco_df.columns.difference([self.target_value_name]))

        X_ex_test = self.kisco_test_df[feature_columns]
        y_ex_test = self.kisco_test_df[self.target_value_name]

        ttt = np.array(X_ex_test.tolist()).reshape(1,-1)

        predict_ex_test = model.predict(ttt)

        print('테스트 = ', y_ex_test)
        print(predict_ex_test)


    ''' 최적 회수율 탐색을 위한 데이터 증폭 '''
    def create_predict_data(self,model, target_value_name, x_value):
        save_amp_df = self.kisco_test_df
        feature_columns = list(self.kisco_test_df.columns.difference([target_value_name]))
        X_ex_test = self.kisco_test_df[feature_columns]
        y_ex_test = self.kisco_test_df[target_value_name]

        print('탐색할 x 값 ========>', X_ex_test[x_value].tolist()[0])
        print('coef ===>', self.fitted_full_model.params[x_value])
        print('coef ===>', self.fitted_full_model.params[x_value])
        # temp_df = hanchul_test_df.copy()
        for i in range(10):
            temp_df = self.kisco_test_df.copy()

            temp_df[x_value] = temp_df[x_value] + (i + 1) * 50  # 일단 50씩 증가 (수식에 의한 계산 필요)
            save_amp_df = pd.concat([save_amp_df, temp_df], ignore_index=True)

        empty_df = pd.DataFrame(columns=self.kisco_test_df.columns)
        for i in range(len(save_amp_df)):
            temp_df = save_amp_df.loc[i].copy()

            temp_df['lance_flux'] = temp_df['lance_flux'] - (i + 1) * 50
            empty_df = empty_df.append(temp_df, ignore_index=True)

        save_amp_df = pd.concat([save_amp_df, empty_df], ignore_index=True)

        value = X_ex_test[x_value].tolist()[0]

        X_ex_test = save_amp_df[feature_columns]
        y_ex_test = save_amp_df[target_value_name]

        predict_ex_test = model.predict(X_ex_test)

        print("예측 결과 predict_ex_test", predict_ex_test)
        print("예측결과 최대값 ", predict_ex_test.max())


    ''' 복사된 데이터를 예측 '''
    def predict_copy_data(self,model, target_value_name):
        feature_columns = list(self.experience_search_df.columns.difference([target_value_name]))
        X_ex_test = self.experience_search_df[feature_columns]
        y_ex_test = self.experience_search_df[target_value_name]


        predict_ex_test = model.predict(X_ex_test)

        print("예측 결과 predict_ex_test", predict_ex_test)
        print("예측결과 최대값 ", predict_ex_test.max())
        print('경험적 탐색 테스트 = ', predict_ex_test)
        print('경험적 탐색 테스트 최대값 = ', max(predict_ex_test))
        print('경험적 탐색 테스트 최소값 = ', min(predict_ex_test))





    ''' 최적 회수율 탐색을 위한 데이터 증폭 '''
    def create_predict_data(self,model, target_value_name, x_value):
        save_amp_df = self.kisco_test_df
        feature_columns = list(self.kisco_test_df.columns.difference([target_value_name]))
        X_ex_test = self.kisco_test_df[feature_columns]
        y_ex_test = self.kisco_test_df[target_value_name]

        print('탐색할 x 값 ========>', X_ex_test[x_value].tolist()[0])
        print('coef ===>', self.fitted_full_model.params[x_value])
        print('coef ===>', self.fitted_full_model.params[x_value])
        # temp_df = hanchul_test_df.copy()
        for i in range(10):
            temp_df = self.kisco_test_df.copy()

            temp_df[x_value] = temp_df[x_value] + (i + 1) * 50  # 일단 50씩 증가 (수식에 의한 계산 필요)
            save_amp_df = pd.concat([save_amp_df, temp_df], ignore_index=True)

        empty_df = pd.DataFrame(columns=self.kisco_test_df.columns)
        for i in range(len(save_amp_df)):
            temp_df = save_amp_df.loc[i].copy()

            temp_df['lance_flux'] = temp_df['lance_flux'] - (i + 1) * 50
            empty_df = empty_df.append(temp_df, ignore_index=True)

        save_amp_df = pd.concat([save_amp_df, empty_df], ignore_index=True)

        value = X_ex_test[x_value].tolist()[0]

        X_ex_test = save_amp_df[feature_columns]
        y_ex_test = save_amp_df[target_value_name]

        predict_ex_test = model.predict(X_ex_test)

        print("예측 결과 predict_ex_test", predict_ex_test)
        print("예측결과 최대값 ", predict_ex_test.max())

    ''' RandomForestRegressor 예측하기 위한 데이터 복제 '''
    ''' target_value_name : 타겟변수  '''
    ''' input_x_values : 사용자에의해 입력된 입력값 '''
    def copy_experience_data(self, target_value_name,input_x_values):
        feature_columns = list(self.kisco_test_df.columns.difference([target_value_name]))
        self.experience_search_df = self.kisco_df.copy()

        #feature_columns = list(self.hanchul_df.columns.difference([self.target_value_name]))

        X_ex_test = self.kisco_test_df[input_x_values]
        size = len(self.experience_search_df)
        #for i in range(size):
        self.experience_search_df.iloc[0:1][input_x_values] = X_ex_test
        #self.experience_search_df.iloc[1:2][input_x_values] = X_ex_test
        #self.experience_search_df.iloc[1][input_x_values] = X_ex_test
        temp_df = self.kisco_test_df[input_x_values]
        save_amp_df = self.kisco_test_df[input_x_values]

        for i in range(size):
            save_amp_df = pd.concat([save_amp_df, temp_df], ignore_index=True)
        self.experience_search_df[input_x_values] = save_amp_df[input_x_values]
        print('값 복제 ' ,self.experience_search_df)




    ''' vif factor 계산 '''
    def get_vif_factor(self):
        vif_df = sm.add_constant(self.kisco_df, has_constant='add')
        # feature_columns = list(vif_df.columns.difference(['회수율']))
        vif = pd.DataFrame()
        vif["VIF Factor"] = [variance_inflation_factor(vif_df.values, i) for i in range(vif_df.shape[1])]
        vif["features"] = vif_df.columns



    ''' osl model 회귀적합 생성'''
    def make_osl_model(self):

        osl_df = sm.add_constant(self.kisco_df, has_constant='add')
        '''target 변수 제외한 컬럼들을 독립변수로 선택'''
        feature_columns = list(osl_df.columns.difference([self.target_value_name]))

        X = osl_df[feature_columns]
        y = osl_df[self.target_value_name]
        train_x, test_x, train_y, test_y = train_test_split(X, y, train_size=0.7, test_size=0.3)

        # Train the MLR / 회귀모델적합
        model = sm.OLS(train_y, train_x)
        self.fitted_full_model = model.fit()







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
    
    



