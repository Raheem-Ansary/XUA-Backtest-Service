import argparse
from datetime import datetime

import backtrader as bt


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Gold (XAUUSD) slippage example",
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
    parser.add_argument("--fromdate", default=None, help="YYYY-MM-DD (optional)")
    parser.add_argument("--todate", default=None, help="YYYY-MM-DD (optional)")
    parser.add_argument("--cash", type=float, default=10000, help="Starting cash")
    parser.add_argument("--fast", type=int, default=10, help="Fast SMA")
    parser.add_argument("--slow", type=int, default=30, help="Slow SMA")
    parser.add_argument(
        "--slippage-fixed",
        type=float,
        default=None,
        help="Fixed slippage (price units)",
    )
    parser.add_argument(
        "--slippage-perc",
        type=float,
        default=None,
        help="Percent slippage (e.g. 0.001 = 0.1%%)",
    )
    parser.add_argument("--plot", action="store_true", help="Plot result")
    return parser


def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d")


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
        fromdate=_parse_date(args.fromdate),
        todate=_parse_date(args.todate),
    )

    cerebro.adddata(data)
    cerebro.addstrategy(SmaCross, fast=args.fast, slow=args.slow)
    cerebro.broker.setcash(args.cash)

    if args.slippage_fixed is not None:
        cerebro.broker.set_slippage_fixed(args.slippage_fixed)
    if args.slippage_perc is not None:
        cerebro.broker.set_slippage_perc(args.slippage_perc)

    cerebro.run()
    if args.plot:
        cerebro.plot(style="candlestick")


if __name__ == "__main__":
    main()
