
from backtesting import Strategy
from util.ATR import *
from util.SMA import *
from util.plot_equity import *
from util.load_data import *


class SMA_crossover(Strategy):
    ATR_SL = 0.5

    def init(self):
        self.data.df['ATR'] = ATR(self.data.df, 20)['ATR']
        self.data.df['sma_fast'] = SMA(self.data.df, 50, 200)['sma_fast']

    def next(self):

        pre_sma_fast = self.data.df.loc[self.data.df.index[-2], 'sma_fast']
        pre_sma_low = self.data.df.loc[self.data.df.index[-2], 'sma_slow']
        current_sma_fast = self.data.df.loc[self.data.df.index[-1], 'sma_fast']
        current_sma_low = self.data.df.loc[self.data.df.index[-1], 'sma_slow']
        current_ATR = self.data.df.loc[self.data.df.index[-1], 'ATR']

        if pre_sma_fast < pre_sma_low and current_sma_fast >= current_sma_low and not self.position:
            tp = self.data.Close[-1] + current_ATR * self.ATR_SL
            sl = self.data.Close[-1] - current_ATR * self.ATR_SL
            # Place your buy logic here
            self.buy(sl=sl, tp=tp, size=1)

        if pre_sma_fast > pre_sma_low and current_sma_fast <= current_sma_low and not self.position:
            tp = self.data.Close[-1] - current_ATR * self.ATR_SL
            sl = self.data.Close[-1] + current_ATR * self.ATR_SL

            self.sell(sl=sl, tp=tp, size=1)
