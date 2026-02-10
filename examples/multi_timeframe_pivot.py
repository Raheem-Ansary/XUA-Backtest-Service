import argparse

import backtrader as bt


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Gold (XAUUSD) multi-timeframe pivot strategy",
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
        "--higher",
        choices=["weekly", "monthly"],
        default="weekly",
        help="Higher timeframe for pivot points",
    )
    parser.add_argument("--plot", action="store_true", help="Plot result")
    return parser


def _tf(value):
    return {
        "weekly": bt.TimeFrame.Weeks,
        "monthly": bt.TimeFrame.Months,
    }[value]


class PivotSignal(bt.Strategy):
    params = dict(use_r1=False)

    def __init__(self):
        self.pivot = bt.ind.PivotPoint(self.data1)

    def next(self):
        if not self.position:
            if self.data0.close[0] > (self.pivot.r1[0] if self.p.use_r1 else self.pivot.p[0]):
                self.buy()
        else:
            if self.data0.close[0] < self.pivot.s1[0]:
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

    cerebro.adddata(data)  # daily
    cerebro.resampledata(data, timeframe=_tf(args.higher))  # higher timeframe

    cerebro.addstrategy(PivotSignal)
    cerebro.run()

    if args.plot:
        cerebro.plot(style="candlestick")


if __name__ == "__main__":
    main()
