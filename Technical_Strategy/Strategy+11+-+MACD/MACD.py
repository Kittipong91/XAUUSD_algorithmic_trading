from backtesting import Strategy
from util.ATR import *
from util.SMA import *
from util.Bollinger_bands import *
from util.load_data import *

class MACD(Strategy):
    ema_s = 12  # EMA Short
    ema_l = 26  # EMA Long
    signal_mw = 9  # Moving Window for Signal Line

    def init(self):
        self.data.df["EMA_S"] = self.data.df['Close'].ewm(
            span=self.ema_s, min_periods=self.ema_s).mean()
        self.data.df["EMA_L"] = self.data.df['Close'].ewm(
            span=self.ema_l, min_periods=self.ema_l).mean()
        self.data.df["MACD"] = self.data.df["EMA_S"] - self.data.df["EMA_L"]
        self.data.df["MACD_Signal"] = self.data.df["MACD"].ewm(
            span=self.signal_mw, min_periods=self.signal_mw).mean()

    def next(self):
        if self.data.df["MACD"].iloc[-1] > self.data.df["MACD_Signal"].iloc[-1] and not self.position.is_long:
            if self.position.is_short:
                self.position.close()
            # Place your buy logic here
            self.buy(size=1)

        if self.data.df["MACD"].iloc[-1] < self.data.df["MACD_Signal"].iloc[-1] and not self.position.is_short:
            if self.position.is_long:
                self.position.close()
            self.sell(size=1)
