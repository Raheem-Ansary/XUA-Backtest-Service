import argparse

import backtrader as bt


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Gold (XAUUSD) multi-data example",
    )
    parser.add_argument(
        "--data",
        default="../data/xauusd_sample.csv",
        help="Primary CSV path (default: ../data/xauusd_sample.csv)",
    )
    parser.add_argument(
        "--data2",
        default="../data/xauusd_sample.csv",
        help="Secondary CSV path (default: ../data/xauusd_sample.csv)",
    )
    parser.add_argument(
        "--dtformat",
        default="%Y-%m-%d",
        help="Datetime format in CSV (default: %%Y-%%m-%%d)",
    )
    parser.add_argument("--plot", action="store_true", help="Plot result")
    return parser


class MultiDataSma(bt.Strategy):
    params = dict(fast=10, slow=30)

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


def main():
    args = build_arg_parser().parse_args()

    cerebro = bt.Cerebro()
    data0 = bt.feeds.GenericCSVData(
        dataname=args.data,
        dtformat=args.dtformat,
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=6,
    )
    data1 = bt.feeds.GenericCSVData(
        dataname=args.data2,
        dtformat=args.dtformat,
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=6,
    )

    cerebro.adddata(data0)
    cerebro.adddata(data1)
    cerebro.addstrategy(MultiDataSma)
    cerebro.run()

    if args.plot:
        cerebro.plot(style="candlestick")


if __name__ == "__main__":
    main()
