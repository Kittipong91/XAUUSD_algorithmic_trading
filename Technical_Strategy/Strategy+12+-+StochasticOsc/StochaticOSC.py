from backtesting import Strategy
import numpy as np
from util.ATR import *
from util.SMA import *
from util.Bollinger_bands import *
from util.load_data import *

class StochasticOSC(Strategy):
    periods = 14
    moving_av = 3

    def init(self):

        self.data.df["roll_low"] = self.data.df['Low'].rolling(
            self.periods).min()
        self.data.df["roll_high"] = self.data.df['High'].rolling(
            self.periods).max()
        self.data.df["K"] = (self.data.df.Close - self.data.df.roll_low) / \
            (self.data.df.roll_high - self.data.df.roll_low) * 100
        self.data.df["D"] = self.data.df.K.rolling(self.moving_av).mean()
        self.data.df["position"] = np.where(
            self.data.df["K"] > self.data.df["D"], 1, -1)

    def next(self):

        k = self.data.df.loc[self.data.df.index[-1], 'K']
        d = self.data.df.loc[self.data.df.index[-1], 'D']
        if k > d:
            if self.position.is_short:
                self.position.close()
            self.buy(size=1)

        if k < d:
            if self.position.is_long:
                self.position.close()
            self.sell(size=1)
