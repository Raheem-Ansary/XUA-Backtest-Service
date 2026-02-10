import backtrader as bt


class SmaCross(bt.Strategy):
    params = dict(
        fast=10,
        slow=30,
    )

    def __init__(self):
        self.sma_fast = bt.ind.SMA(self.data.close, period=self.p.fast)
        self.sma_slow = bt.ind.SMA(self.data.close, period=self.p.slow)
        self.crossover = bt.ind.CrossOver(self.sma_fast, self.sma_slow)

    def next(self):
        if not self.position and self.crossover > 0:
            self.buy()
        elif self.position and self.crossover < 0:
            self.close()


class RsiMeanRevert(bt.Strategy):
    params = dict(
        period=14,
        lower=30,
        upper=70,
    )

    def __init__(self):
        self.rsi = bt.ind.RSI(self.data.close, period=self.p.period)

    def next(self):
        if not self.position and self.rsi < self.p.lower:
            self.buy()
        elif self.position and self.rsi > self.p.upper:
            self.close()


class MultiDataSma(bt.Strategy):
    params = dict(
        fast=10,
        slow=30,
    )

    def __init__(self):
        self.sma0_fast = bt.ind.SMA(self.data0.close, period=self.p.fast)
        self.sma0_slow = bt.ind.SMA(self.data0.close, period=self.p.slow)
        self.sma1_fast = bt.ind.SMA(self.data1.close, period=self.p.fast)
        self.sma1_slow = bt.ind.SMA(self.data1.close, period=self.p.slow)

    def next(self):
        bull0 = self.sma0_fast[0] > self.sma0_slow[0]
        bull1 = self.sma1_fast[0] > self.sma1_slow[0]

        if not self.position and bull0 and bull1:
            self.buy(data=self.data0)
        elif self.position and (not bull0 or not bull1):
            self.close(data=self.data0)
