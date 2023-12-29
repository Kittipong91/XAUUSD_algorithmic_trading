from backtesting import Strategy
import numpy as np
from util.ATR import *
from util.SMA import *

class Martingale(Strategy):
    ATR_SL = 0.5

    def init(self):
        self.data.df['ATR'] = ATR(self.data.df, 20)['ATR']
        self.data.df['direction'] = np.where(
            self.data.df['Close'] > self.data.df['Open'], 'bull', 'bear')
        self.data.df['dir_count'] = self.data.df.groupby(
            (self.data.df['direction'] != self.data.df['direction'].shift(1)).cumsum()).cumcount()+1

    def next(self):

        mean = self.data.df['ATR'].mean()

        if not self.position and self.data.df['direction'][-1] == 'bear' and mean > 0:
            tp = self.data.df['Close'][-1] + mean
            sl = self.data.df['Close'][-1] - mean
            # Place your buy logic here
            self.buy(sl=sl, tp=tp, size=1)

        if not self.position and self.data.df['direction'][-1] == 'bull' and mean > 0:
            tp = self.data.df['Close'][-1] - mean
            sl = self.data.df['Close'][-1] + mean

            self.sell(sl=sl, tp=tp, size=1)
