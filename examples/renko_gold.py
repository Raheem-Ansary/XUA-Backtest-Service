import argparse

import backtrader as bt


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Gold (XAUUSD) Renko example",
    )
    parser.add_argument(
        "--data",
        default="../data/xauusd_sample.csv",
        help="CSV path (default: ../data/xauusd_sample.csv)",
    )
    parser.add_argument(
        "--dtformat",
        default="%Y-%m-%d",
        help="Datetime format in CSV (default: %%Y-%%m-%%d)",
    )
    parser.add_argument(
        "--brick",
        type=float,
        default=5.0,
        help="Renko brick size",
    )
    parser.add_argument("--plot", action="store_true", help="Plot result")
    return parser


class SmaCross(bt.Strategy):
    params = dict(fast=10, slow=30)

    def __init__(self):
        fast = bt.ind.SMA(self.data.close, period=self.p.fast)
        slow = bt.ind.SMA(self.data.close, period=self.p.slow)
        self.crossover = bt.ind.CrossOver(fast, slow)

    def next(self):
        if not self.position and self.crossover > 0:
            self.buy()
        elif self.position and self.crossover < 0:
            self.close()


def main():
    args = build_arg_parser().parse_args()

    cerebro = bt.Cerebro()
    data = bt.feeds.GenericCSVData(
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

    data.addfilter(bt.filters.Renko, bricksize=args.brick)
    cerebro.adddata(data)
    cerebro.addstrategy(SmaCross)
    cerebro.run()

    if args.plot:
        cerebro.plot(style="candlestick")


if __name__ == "__main__":
    main()
