from backtesting import Strategy


class BuyAndHold(Strategy):

    def init(self):
        pass

    def next(self):
        if self.position:
            self.position.close()
            self.buy(size=1)
        elif not self.position:
            self.buy(size=1)
