from backtesting import Backtest, Strategy
from util.ATR import *
import numpy as np

class Momentum(Strategy):
    ATR_SL = 6
    max_dir_count = 2

    def init(self):
        self.data.df['ATR'] = ATR(self.data.df, 20)['ATR']
        self.data.df['direction'] = np.where(
            self.data.Close > self.data.Open, 'bull', 'bear')
        self.data.df['dir_count'] = self.data.df.groupby(
            (self.data.df['direction'] != self.data.df['direction'].shift(1)).cumsum()).cumcount()+1

    def next(self):
        current_dir_count = self.data.df.loc[self.data.df.index[-1], 'dir_count']
        current_direction = self.data.df.loc[self.data.df.index[-1], 'direction']
        current_ATR = self.data.df.loc[self.data.df.index[-1], 'ATR']

        if current_dir_count >= self.max_dir_count and current_direction == 'bull' and not self.position and not np.isnan(current_ATR):
            if self.position.is_long:
                print('Have a order')
            tp = self.data.Close[-1] + current_ATR * self.ATR_SL
            sl = self.data.Open[-1] - 0.001

            # Place your buy logic here

            self.buy(sl=sl, tp=tp, size=1)
        if current_dir_count >= self.max_dir_count and current_direction == 'bear' and not self.position and not np.isnan(current_ATR):
            tp = self.data.Close[-1] - current_ATR * self.ATR_SL
            sl = self.data.Open[-1] + 0.001

            self.sell(sl=sl, tp=tp, size=1)
