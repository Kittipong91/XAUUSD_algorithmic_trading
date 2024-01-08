from config.constants import *
from backtesting import Strategy
from util.ATR import *
from util.SMA import *
from util.Bollinger_bands import *

class Bolinger_bands(Strategy):
    ATR_SL = 0.5
    Mutiple_TP = 10

    band_Low =3
    band_High = 50

    def init(self):
        self.data.df['ATR'] = ATR(self.data.df, 20)['ATR']
        self.data.df['sma_fast'] = SMA(self.data.df, 50, 200)['sma_fast']

        self.data.df['upper_band'] = Bollinger_bands(
            self.data.df, self.band_High, self.band_Low)['upper_band']

    def next(self):

        sma_fast = self.data.df.loc[self.data.df.index[-2], 'sma_fast']
        sma_low = self.data.df.loc[self.data.df.index[-2], 'sma_slow']
        current_ATR = self.data.df.loc[self.data.df.index[-1], 'ATR']

        if not self.position and sma_fast >= sma_low and any(self.data.df['Close'][-3: -1].values) <= any(self.data.df['lower_band'][-3: -1].values) and self.data.df['Close'][-1] >= self.data.df['rolling_mean'][-1]:
            tp = self.data.Close + current_ATR * self.ATR_SL * self.Mutiple_TP
            sl = self.data.Close - current_ATR * self.ATR_SL
            # Place your buy logic here
            self.buy(sl=sl, tp=tp, size=1)

        if not self.position and sma_fast <= sma_low and any(self.data.df['Close'][-3: -1].values) >= any(self.data.df['lower_band'][-3: -1].values) and self.data.df['Close'][-1] <= self.data.df['rolling_mean'][-1]:
            tp = self.data.Close - current_ATR * self.ATR_SL * self.Mutiple_TP
            sl = self.data.Close + current_ATR * self.ATR_SL

            self.sell(sl=sl, tp=tp, size=1)
