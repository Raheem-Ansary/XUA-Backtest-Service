import argparse
from datetime import datetime

import backtrader as bt


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Gold (XAUUSD) commission schemes example",
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
    parser.add_argument("--stake", type=int, default=1, help="Position size")
    parser.add_argument(
        "--commtype",
        choices=["none", "perc", "fixed"],
        default="perc",
        help="Commission type",
    )
    parser.add_argument(
        "--commission",
        type=float,
        default=0.0002,
        help="Commission value",
    )
    parser.add_argument("--mult", type=int, default=1, help="Multiplier")
    parser.add_argument("--margin", type=float, default=0.0, help="Margin")
    parser.add_argument(
        "--stocklike",
        action="store_true",
        help="Use stock-like commission model",
    )
    parser.add_argument(
        "--percrel",
        action="store_true",
        help="Interpret perc as relative (xx%%) instead of absolute 0.xx",
    )
    parser.add_argument("--plot", action="store_true", help="Plot result")
    return parser


def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d")


class BuyHold(bt.Strategy):
    def __init__(self):
        self.bought = False

    def next(self):
        if not self.bought:
            self.buy(size=self.p.stake)
            self.bought = True


BuyHold.params = dict(stake=1)


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
    cerebro.addstrategy(BuyHold, stake=args.stake)
    cerebro.broker.setcash(args.cash)

    commtypes = {
        "none": None,
        "perc": bt.CommInfoBase.COMM_PERC,
        "fixed": bt.CommInfoBase.COMM_FIXED,
    }

    cerebro.broker.setcommission(
        commission=args.commission,
        mult=args.mult,
        margin=args.margin,
        percabs=not args.percrel,
        commtype=commtypes[args.commtype],
        stocklike=args.stocklike,
    )

    cerebro.run()
    if args.plot:
        cerebro.plot(style="candlestick")


if __name__ == "__main__":
    main()
