import sys
sys.path.append('../../')

from util.Save_result_return import save_to_csv


import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from backtesting import Strategy
from backtesting import Backtest
plt.style.use("seaborn-v0_8")


class ML_Regression():

    def __init__(self, data, strategy, start_train, start_test, end_train, end_test, TF):
        self.data = data
        self.strategy = strategy
        self.start_train = start_train
        self.start_test = start_test
        self.end_train = end_train
        self.end_test = end_test
        self.TF = TF
        self.data_train = None
        self.data_test = None
        self.results = None
        self.model = None

    def Prepare(self, lags=5):
        data = self.data.loc[self.start_train:self.end_train].copy()
        data["returns"] = np.log(data['Close'].div(data['Close'].shift(1)))
        data.dropna(inplace=True)
        cols = []

        for lag in range(1, lags + 1):
            col = "lag{}".format(lag)
            data[col] = data['returns'].shift(lag)
            cols.append(col)
        data.dropna(inplace=True)

        lm = LinearRegression(fit_intercept=True)
        lm.fit(data[cols], data['returns'])
        data["pred"] = lm.predict(data[cols])
        data['pred'] = np.sign(data['pred'])

        self.model = lm
        self.data_train = data

    def Predict(self, lags=5):
        data = self.data.loc[self.start_test:self.end_test].copy()
        data["returns"] = np.log(data['Close'].div(data['Close'].shift(1)))
        cols = []

        for lag in range(1, lags + 1):
            col = "lag{}".format(lag)
            data[col] = data['returns'].shift(lag)
            cols.append(col)
        data.dropna(inplace=True)

        data["pred"] = self.model.predict(data[cols])
        data['pred'] = np.sign(data['pred'])

        self.data_test = data

    def Backtest(self, data, account_size=2000):
        # Assuming you have a Backtest class that performs backtesting
        backtest = Backtest(data, self.strategy,
                            cash=account_size, margin=1 / 2000)
        result = backtest.run()
        return result

    def Save_Result(self, result, filepath):

        save_to_csv(result,filepath)
      

    def Run(self):
        self.Prepare()
        result_train = self.Backtest(self.data_train)
        filename_train = f'result_{self.TF}_In_Sample.csv'
        filepath_train = f'../../out/Machine_Learning/Multiple_Linear_Regression/Backtest/train.csv'
        self.Save_Result(result_train, filepath_train)

        self.Predict()
        result_test = self.Backtest(self.data_test)
        filename_test = f'result_{self.TF}_Out_Sample.csv'
        filepath_test = f'../../out/Machine_Learning/Multiple_Linear_Regression/Backtest/test.csv'
        self.Save_Result(result_test, filepath_test)

        return result_train , result_test

        


        
