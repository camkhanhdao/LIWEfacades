#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 01:36:39 2018
@author: camkhanhdao
"""
import numpy as np
import pandas as pd
from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import CleanData
import credentials

regression_path = credentials.get_path("regression_path")

modules = ['v1', 'v2', 'v3', 'v4']
titles = ['Module 1', 'Module 2', 'Module 3', 'Module 4']
PV_dict = {1: 'v1', 2: 'v2', 3: 'v3', 4: 'v4'}

df = CleanData.main_merge()


class Regression:

    def __init__(self,module='v1', path_name=regression_path):
        self.path_name = path_name
        self.module = module

    def regression(self):
        regression = df.drop(['hum_index', 'irr_index', 'T_index'],axis=1).astype(np.float64)
        y, X = dmatrices('{} ~ irr + T + hum'.format(self.module), data=regression, return_type="dataframe")
        result = sm.OLS(y, X).fit()
        vif_df = pd.DataFrame()
        vif_df["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        vif_df["variance"] = X.columns
        with open(regression_path+'{} summary.txt'.format(self.module), 'w+') as file:
            file.write(result.summary().as_text()+'\n')
        vif_df.to_csv(r'{}{} summary.txt'.format(regression_path,self.module),
                      header=None, index=None, sep=' ', mode='a')
        return result.summary()

