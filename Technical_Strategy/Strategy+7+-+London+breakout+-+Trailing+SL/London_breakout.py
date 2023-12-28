from backtesting import Strategy
from util.ATR import *
from util.SMA import *
import numpy as np

class London_breakout(Strategy):
    ATR_SL = 0.5
    entry_time = 8

    def init(self):
        self.data.df['ATR'] = ATR(self.data.df, 20)['ATR']
        self.data.df['london_opening'] = np.where(
            (self.data.df.index.hour + 1) == self.entry_time, True, False)

    def next(self):

        current_ATR = self.data.df.loc[self.data.df.index[-1], 'ATR']

        if not self.position and self.data.df['london_opening'][-1] == True and self.data.df['Close'][-1] >= self.data.df['Close'].rolling(8).max()[-1]:
            tp = self.data.Close + current_ATR * self.ATR_SL * 5
            sl = self.data.Close - current_ATR * self.ATR_SL
            # Place your buy logic here
            self.buy(sl=sl, tp=tp, size=1)

        if not self.position and self.data.df['london_opening'][-1] == True and self.data.df['Close'][-1] <= self.data.df['Close'].rolling(8).min()[-1]:
            tp = self.data.Close - current_ATR * self.ATR_SL * 5
            sl = self.data.Close + current_ATR * self.ATR_SL

            self.sell(sl=sl, tp=tp, size=1)
