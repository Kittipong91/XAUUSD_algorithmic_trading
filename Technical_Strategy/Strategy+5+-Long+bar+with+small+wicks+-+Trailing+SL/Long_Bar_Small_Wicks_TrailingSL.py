from backtesting import  Strategy
from util.ATR import *
from util.SMA import *
from util.RSI import *
from util.LongBarSmallWick import *

class Long_Bar_Small_Wicks_TrailingSL(Strategy):
    ATR_SL = 0.5

    def init(self):
        self.data.df['ATR'] = ATR(self.data.df, 20)['ATR']
        self.data.df['average_bar'] = average_bar_size(self.data.df)[
            'average_bar']
        self.data.df['small_wick'] = small_wick(
            self.data.df, 0.2)['small_wick']

    def next(self):

        current_ATR = self.data.df.loc[self.data.df.index[-1], 'ATR']

        if (self.data.df['High'][-2] - self.data.df['Low'][-2]) >= 4 * self.data.df['average_bar'][-2] and self.data.df['small_wick'][-2] == True \
                and self.data.df['Close'][-2] > self.data.df['Open'][-2] and not self.position:
            tp = self.data.Close + current_ATR * self.ATR_SL * 10
            sl = self.data.Close - current_ATR * self.ATR_SL
            # Place your buy logic here
            self.buy(sl=sl, tp=tp, size=1)

        if (self.data.df['High'][-2] - self.data.df['Low'][-2]) >= 4 * self.data.df['average_bar'][-2] and self.data.df['small_wick'][-2] == True \
                and self.data.df['Close'][-2] < self.data.df['Open'][-2] and not self.position:
            tp = self.data.Close - current_ATR * self.ATR_SL * 10
            sl = self.data.Close + current_ATR * self.ATR_SL

            self.sell(sl=sl, tp=tp, size=1)
