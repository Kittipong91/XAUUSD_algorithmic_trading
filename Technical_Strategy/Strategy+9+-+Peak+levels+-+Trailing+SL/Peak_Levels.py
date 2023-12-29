from backtesting import Strategy
from util.ATR import ATR
from scipy.signal import argrelextrema
import numpy as np

class Peak_Levels(Strategy):
    ATR_SL = 0.5
    support = []
    resist = []

    def init(self):
        self.data.df['ATR'] = ATR(self.data.df, 20)['ATR']
        self.price = self.data.df['Close']
        self.minima_indices = argrelextrema(
            self.price.values, np.less_equal, order=100)[0]
        self.maxima_indices = argrelextrema(
            self.price.values, np.greater_equal, order=100)[0]
        self.data.df.loc[self.data.df.index[self.minima_indices],
                         'min'] = self.price.iloc[self.minima_indices]
        self.data.df.loc[self.data.df.index[self.maxima_indices],
                         'max'] = self.price.iloc[self.maxima_indices]

    def next(self):

        if len(self.data.df) >= 12:

            if (self.data.df['max'][-12] != None and self.data.df['max'][-12] > 0):
                self.resist.append(self.data.df['max'][-12])
            elif (self.data.df['min'][-12] != None and self.data.df['min'][-12]) > 0:
                self.support.append(self.data.df['min'][-12])

        current_ATR = self.data.df.loc[self.data.df.index[-1], 'ATR']

        if self.support != [] and any(self.data.df['Close'][-1] > s for s in self.support) and any(self.data.df['Close'][-1] <= s for s in self.support) and not self.position and not np.isnan(current_ATR):
            tp = self.data.Close + current_ATR * self.ATR_SL
            sl = self.data.Close - current_ATR * self.ATR_SL
            # Place your buy logic here
            self.buy(sl=sl, tp=tp, size=1)

        if self.resist != [] and any(self.data.df['Close'][-1] < r for r in self.resist) and any(self.data.df['Close'][-1] >= r for r in self.resist) and not self.position and not np.isnan(current_ATR):
            tp = self.data.Close - current_ATR * self.ATR_SL
            sl = self.data.Close + current_ATR * self.ATR_SL

            self.sell(sl=sl, tp=tp, size=1)
