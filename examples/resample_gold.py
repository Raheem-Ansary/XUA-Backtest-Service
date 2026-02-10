import argparse

import backtrader as bt


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Resample Gold (XAUUSD) data to higher timeframes",
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
        "--timeframe",
        choices=["daily", "weekly", "monthly"],
        default="weekly",
        help="Resample target timeframe",
    )
    parser.add_argument(
        "--compression",
        type=int,
        default=1,
        help="Compression (default: 1)",
    )
    parser.add_argument("--plot", action="store_true", help="Plot result")
    return parser


def _tf(value):
    return {
        "daily": bt.TimeFrame.Days,
        "weekly": bt.TimeFrame.Weeks,
        "monthly": bt.TimeFrame.Months,
    }[value]


def main():
    args = build_arg_parser().parse_args()

    cerebro = bt.Cerebro(stdstats=False)
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

    cerebro.resampledata(
        data,
        timeframe=_tf(args.timeframe),
        compression=args.compression,
    )

    cerebro.addstrategy(bt.Strategy)
    cerebro.run()
    if args.plot:
        cerebro.plot(style="candlestick")


if __name__ == "__main__":
    main()
