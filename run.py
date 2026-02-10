import argparse
from datetime import datetime
from pathlib import Path

import backtrader as bt

from strategies import MultiDataSma, RsiMeanRevert, SmaCross


def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d")


def _parse_timeframe(value):
    mapping = {
        "ticks": bt.TimeFrame.Ticks,
        "seconds": bt.TimeFrame.Seconds,
        "minutes": bt.TimeFrame.Minutes,
        "days": bt.TimeFrame.Days,
        "weeks": bt.TimeFrame.Weeks,
        "months": bt.TimeFrame.Months,
        "years": bt.TimeFrame.Years,
    }
    key = value.strip().lower()
    if key not in mapping:
        raise argparse.ArgumentTypeError(
            "timeframe must be one of: ticks, seconds, minutes, days, weeks, months, years"
        )
    return mapping[key]

def _count_csv_rows(path):
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"Data file not found: {path}")
    rows = 0
    with p.open("r", encoding="utf-8") as f:
        first = f.readline()
        for line in f:
            if line.strip():
                rows += 1
    if rows == 0:
        # handle no header or empty file
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows += 1
    return rows


def _strategy_min_bars(args):
    if args.strategy == "sma_cross":
        return max(args.fast, args.slow)
    if args.strategy == "rsi_revert":
        return args.rsi_period
    if args.strategy == "multi_sma":
        return max(args.fast, args.slow)
    return 0


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Gold (XAUUSD) backtest tool powered by Backtrader",
    )
    parser.add_argument(
        "--data",
        default="data/xauusd_sample.csv",
        help="CSV path (default: data/xauusd_sample.csv)",
    )
    parser.add_argument(
        "--data2",
        default=None,
        help="Second CSV path for multi-data mode (default: none)",
    )
    parser.add_argument(
        "--dtformat",
        default="%Y-%m-%d",
        help="Datetime format in CSV (default: %%Y-%%m-%%d)",
    )
    parser.add_argument("--datecol", type=int, default=0, help="Date column index")
    parser.add_argument("--opencol", type=int, default=1, help="Open column index")
    parser.add_argument("--highcol", type=int, default=2, help="High column index")
    parser.add_argument("--lowcol", type=int, default=3, help="Low column index")
    parser.add_argument("--closecol", type=int, default=4, help="Close column index")
    parser.add_argument(
        "--volumecol",
        type=int,
        default=5,
        help="Volume column index (-1 if not available)",
    )
    parser.add_argument(
        "--openinterestcol",
        type=int,
        default=6,
        help="OpenInterest column index (-1 if not available)",
    )
    parser.add_argument(
        "--timeframe",
        type=_parse_timeframe,
        default=bt.TimeFrame.Days,
        help="Data timeframe (days, minutes, ...)",
    )
    parser.add_argument(
        "--compression",
        type=int,
        default=1,
        help="Timeframe compression (default: 1)",
    )
    parser.add_argument(
        "--fromdate",
        type=_parse_date,
        default=None,
        help="YYYY-MM-DD (optional)",
    )
    parser.add_argument(
        "--todate",
        type=_parse_date,
        default=None,
        help="YYYY-MM-DD (optional)",
    )
    parser.add_argument("--cash", type=float, default=10000, help="Starting cash")
    parser.add_argument(
        "--commission",
        type=float,
        default=0.0002,
        help="Commission rate (e.g. 0.0002 = 0.02%%)",
    )
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
    parser.add_argument(
        "--coc",
        action="store_true",
        help="Cheat-on-close (execute at close price)",
    )
    parser.add_argument(
        "--coo",
        action="store_true",
        help="Cheat-on-open (execute at next open price)",
    )
    parser.add_argument(
        "--sizer",
        choices=["fixed", "percent"],
        default="fixed",
        help="Position sizing method",
    )
    parser.add_argument(
        "--stake",
        type=int,
        default=1,
        help="Fixed stake size (used with --sizer fixed)",
    )
    parser.add_argument(
        "--stake-percent",
        type=float,
        default=10,
        help="Percent of cash per trade (used with --sizer percent)",
    )
    parser.add_argument(
        "--strategy",
        choices=["sma_cross", "rsi_revert", "multi_sma"],
        default="sma_cross",
        help="Strategy selection",
    )
    parser.add_argument(
        "--mode",
        choices=["standard", "renko", "multi"],
        default="standard",
        help="Run mode (standard, renko, multi)",
    )
    parser.add_argument(
        "--renko-brick",
        type=float,
        default=5.0,
        help="Renko brick size (used with --mode renko)",
    )
    parser.add_argument("--fast", type=int, default=10, help="Fast SMA period")
    parser.add_argument("--slow", type=int, default=30, help="Slow SMA period")
    parser.add_argument("--rsi-period", type=int, default=14, help="RSI period")
    parser.add_argument("--rsi-lower", type=int, default=30, help="RSI lower band")
    parser.add_argument("--rsi-upper", type=int, default=70, help="RSI upper band")
    parser.add_argument(
        "--analyzers",
        action="store_true",
        help="Print analyzers (returns, drawdown, sharpe, trades)",
    )
    parser.add_argument("--plot", action="store_true", help="Plot result")
    return parser


def _add_strategy(cerebro, args):
    if args.strategy == "sma_cross":
        cerebro.addstrategy(SmaCross, fast=args.fast, slow=args.slow)
    elif args.strategy == "rsi_revert":
        cerebro.addstrategy(
            RsiMeanRevert,
            period=args.rsi_period,
            lower=args.rsi_lower,
            upper=args.rsi_upper,
        )
    elif args.strategy == "multi_sma":
        cerebro.addstrategy(MultiDataSma, fast=args.fast, slow=args.slow)


def _add_sizer(cerebro, args):
    if args.sizer == "fixed":
        cerebro.addsizer(bt.sizers.FixedSize, stake=args.stake)
    else:
        cerebro.addsizer(bt.sizers.PercentSizer, percents=args.stake_percent)


def _add_analyzers(cerebro):
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")


def _print_analyzers(results):
    analysis = results[0].analyzers
    drawdown = analysis.drawdown.get_analysis()
    sharpe = analysis.sharpe.get_analysis()
    returns = analysis.returns.get_analysis()
    trades = analysis.trades.get_analysis()

    print("Analyzers:")
    if drawdown:
        print(f"  Max Drawdown: {drawdown.get('max', {}).get('drawdown', 0):.2f}%")
    if sharpe:
        print(f"  Sharpe Ratio: {sharpe.get('sharperatio')}")
    if returns:
        print(f"  Total Return: {returns.get('rtot')}")
        print(f"  Annual Return: {returns.get('rnorm')}")
    if trades:
        total = trades.get("total", {}).get("total")
        won = trades.get("won", {}).get("total")
        lost = trades.get("lost", {}).get("total")
        print(f"  Trades: total={total} won={won} lost={lost}")


def main():
    args = build_arg_parser().parse_args()

    cerebro = bt.Cerebro()
    _add_sizer(cerebro, args)

    data_rows = _count_csv_rows(args.data)
    if args.mode == "multi":
        if not args.data2:
            raise SystemExit("In multi mode, --data2 is required.")
        data2_rows = _count_csv_rows(args.data2)
        data_rows = min(data_rows, data2_rows)

    min_bars = _strategy_min_bars(args)
    if data_rows <= min_bars:
        print(
            "Warning: data length is smaller than strategy period. "
            "Adjusting periods to fit the data."
        )
        if args.strategy in ("sma_cross", "multi_sma"):
            args.slow = max(2, data_rows - 1)
            args.fast = max(1, min(args.fast, args.slow - 1))
        elif args.strategy == "rsi_revert":
            args.rsi_period = max(2, data_rows - 1)

    data = bt.feeds.GenericCSVData(
        dataname=args.data,
        dtformat=args.dtformat,
        datetime=args.datecol,
        open=args.opencol,
        high=args.highcol,
        low=args.lowcol,
        close=args.closecol,
        volume=args.volumecol,
        openinterest=args.openinterestcol,
        fromdate=args.fromdate,
        todate=args.todate,
        timeframe=args.timeframe,
        compression=args.compression,
        nullvalue=0.0,
    )

    if args.mode == "renko":
        data.addfilter(bt.filters.Renko, bricksize=args.renko_brick)

    cerebro.adddata(data)

    if args.mode == "multi":
        data2 = bt.feeds.GenericCSVData(
            dataname=args.data2,
            dtformat=args.dtformat,
            datetime=args.datecol,
            open=args.opencol,
            high=args.highcol,
            low=args.lowcol,
            close=args.closecol,
            volume=args.volumecol,
            openinterest=args.openinterestcol,
            fromdate=args.fromdate,
            todate=args.todate,
            timeframe=args.timeframe,
            compression=args.compression,
            nullvalue=0.0,
        )
        cerebro.adddata(data2)
        args.strategy = "multi_sma"

    _add_strategy(cerebro, args)
    cerebro.broker.setcash(args.cash)
    cerebro.broker.setcommission(commission=args.commission)
    if args.slippage_fixed is not None:
        cerebro.broker.set_slippage_fixed(args.slippage_fixed)
    if args.slippage_perc is not None:
        cerebro.broker.set_slippage_perc(args.slippage_perc)
    if args.coc:
        cerebro.broker.set_coc(True)
    if args.coo:
        cerebro.broker.set_coo(True)

    if args.analyzers:
        _add_analyzers(cerebro)

    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    results = cerebro.run()
    print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

    if args.analyzers:
        _print_analyzers(results)

    if args.plot:
        try:
            cerebro.plot(style="candlestick")
        except ImportError:
            raise SystemExit(
                "Plotting requires matplotlib. Install with: pip install matplotlib"
            )


if __name__ == "__main__":
    main()
