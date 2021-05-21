import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split

import time
import itertools

class ValueSelect() :
    def __init__(self):
        pass



    def process_subset(self,X, y, feature_set):
        model = sm.OLS(y, X[list(feature_set)])  # Modeling
        regr = model.fit()  # 모델 학습
        AIC = regr.aic  # 모델의 AIC
        return {"model": regr, "AIC": AIC}

    ########전진선택법(step=1)

    def forward(self,X, y, predictors):
        # 데이터 변수들이 미리정의된 predictors에 있는지 없는지 확인 및 분류
        remaining_predictors = [p for p in X.columns.difference(['const']) if p not in predictors]
        tic = time.time()
        results = []
        for p in remaining_predictors:
            results.append(self.process_subset(X=X, y= y, feature_set=predictors+[p]+['const']))
        # 데이터프레임으로 변환
        models = pd.DataFrame(results)

        # AIC가 가장 낮은 것을 선택
        best_model = models.loc[models['AIC'].argmin()] # index
        toc = time.time()
        print("Processed ", models.shape[0], "models on", len(predictors)+1, "predictors in", (toc-tic))
        print('Selected predictors:',best_model['model'].model.exog_names,' AIC:',best_model[0] )
        return best_model



    #### 전진선택법 모델

    def forward_model(self,X,y):
        Fmodels = pd.DataFrame(columns=["AIC", "model"])
        tic = time.time()
        # 미리 정의된 데이터 변수
        predictors = []
        # 변수 1~10개 : 0~9 -> 1~10
        for i in range(1, len(X.columns.difference(['const'])) + 1):
            Forward_result = self.forward(X=X,y=y,predictors=predictors)
            if i > 1:
                if Forward_result['AIC'] > Fmodel_before:
                    break
            Fmodels.loc[i] = Forward_result
            predictors = Fmodels.loc[i]["model"].model.exog_names
            Fmodel_before = Fmodels.loc[i]["AIC"]
            predictors = [ k for k in predictors if k != 'const']
        toc = time.time()
        print("Total elapsed time:", (toc - tic), "seconds.")

        return(Fmodels['model'][len(Fmodels['model'])])

    # getBest: 가장 낮은 AIC를 가지는 모델 선택 및 저장
    def get_best(self,X, y, k):
        tic = time.time()  # 시작시간
        results = []  # 결과 저장공간
        for combo in itertools.combinations(X.columns.difference(['const']), k):  # 각 변수조합을 고려한 경우의 수
            combo = (list(combo) + ['const'])

            results.append(self.process_subset(X, y, feature_set=combo))  # 모델링된 것들을 저장
        models = pd.DataFrame(results)  # 데이터 프레임으로 변환
        # 가장 낮은 AIC를 가지는 모델 선택 및 저장
        best_model = models.loc[models['AIC'].argmin()]  # index
        toc = time.time()  # 종료시간
        print("Processed ", models.shape[0], "models on", k, "predictors in", (toc - tic),
              "seconds.")
        return best_model
