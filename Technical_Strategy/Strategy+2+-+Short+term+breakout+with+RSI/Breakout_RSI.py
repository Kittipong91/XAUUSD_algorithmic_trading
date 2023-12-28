
from backtesting import Strategy
from util.ATR import *
from util.plot_equity import *
from util.load_data import *
from util.RSI import *


class Breakout_RSI(Strategy):
    ATR_SL = 0.5

    def init(self):
        self.data.df['ATR'] = ATR(self.data.df, 20)['ATR']
        self.data.df['RSI'] = rsi(self.data.df, 14)['RSI']
        self.data.df['average_close'] = self.data.df['Close'].rolling(5).mean()

    def next(self):

        rsi = self.data.df.loc[self.data.df.index[-2], 'RSI']
        pre_average_close = self.data.df.loc[self.data.df.index[-2],
                                             'average_close']
        current_average_close = self.data.df.loc[self.data.df.index[-1],
                                                 'average_close']

        current_ATR = self.data.df.loc[self.data.df.index[-1], 'ATR']

        if rsi < 20 and self.data.df['Close'][-1] < pre_average_close and self.data.df['Close'][-1] >= current_average_close and not self.position:
            tp = self.data.Close + current_ATR * self.ATR_SL
            sl = self.data.Close - current_ATR * self.ATR_SL
            # Place your buy logic here
            self.buy(sl=sl, tp=tp, size=1)

        if rsi < 80 and self.data.df['Close'][-1] > pre_average_close and self.data.df['Close'][-1] <= current_average_close and not self.position:
            tp = self.data.Close - current_ATR * self.ATR_SL
            sl = self.data.Close + current_ATR * self.ATR_SL

            self.sell(sl=sl, tp=tp, size=1)
