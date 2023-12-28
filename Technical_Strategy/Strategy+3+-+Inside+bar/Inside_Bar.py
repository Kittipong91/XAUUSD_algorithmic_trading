from backtesting import Strategy
from util.ATR import *
from util.plot_equity import *
from util.load_data import *
from util.SMA import *
import numpy as np

class Inside_Bar(Strategy):
    ATR_SL = 0.5

    def init(self):
        self.data.df['ATR'] = ATR(self.data.df, 20)['ATR']
        self.data.df['sma_fast'] = SMA(self.data.df, 50, 200)['sma_fast']

        self.data.df['inside_bar'] = np.where(((self.data.df['High'] < self.data.df['High'].shift(
            1)) & (self.data.df['Low'] > self.data.df['Low'].shift(1))), True, False)

    def next(self):
        pre_inside_bar = False
        current_inside_bar = False
        if len(self.data.df) >= 3:
            current_inside_bar = self.data.df.loc[self.data.df.index[-2], 'inside_bar']
            pre_inside_bar = self.data.df.loc[self.data.df.index[-3], 'inside_bar']
        sma_fast = self.data.df.loc[self.data.df.index[-2], 'sma_fast']
        sma_low = self.data.df.loc[self.data.df.index[-2], 'sma_slow']
        current_ATR = self.data.df.loc[self.data.df.index[-1], 'ATR']

        if current_inside_bar == True and pre_inside_bar == True and not self.position and sma_fast >= sma_low and self.data.Close > self.data.Open:
            tp = self.data.Close + current_ATR * self.ATR_SL
            sl = self.data.Close - current_ATR * self.ATR_SL
            # Place your buy logic here
            self.buy(sl=sl, tp=tp, size=1)

        if current_inside_bar == True and pre_inside_bar == True and not self.position and sma_fast <= sma_low and self.data.Close < self.data.Open:
            tp = self.data.Close - current_ATR * self.ATR_SL
            sl = self.data.Close + current_ATR * self.ATR_SL

            self.sell(sl=sl, tp=tp, size=1)
