# نمونه‌ها (Examples)


## 1) Resample تایم‌فریم

```bash
python examples/resample_gold.py --timeframe weekly --compression 1 --plot
```

## 2) چندتایم‌فریم + Pivot Point

```bash
python examples/multi_timeframe_pivot.py --higher weekly --plot
```

## 3) اسلیپیج روی استراتژی SMA

```bash
python examples/slippage_gold.py --slippage-perc 0.001 --plot
```

## 4) انواع کمیسیون

```bash
python examples/commission_gold.py --commtype perc --commission 0.0002 --plot
```

## 5) Renko برای طلا

```bash
python examples/renko_gold.py --brick 5 --plot
```

## 6) چند دیتافید هم‌زمان

```bash
python examples/multi_data_gold.py --data ../data/xauusd_sample.csv --data2 ../data/xauusd_sample.csv --plot
```
