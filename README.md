# ابزار بک‌تست طلا (XAUUSD) با Backtrader

این پروژه یک ابزار کامل و سرراست برای بک‌تست بازار طلاست. هدف این است که کاربر با کمترین ابهام بتواند نیازش را برطرف کند.

مالک و صاحب امتیاز: **Raheem-Ansary**

## شروع سریع برای افراد کاملاً مبتدی

این بخش طوری نوشته شده که اگر هیچ تجربه‌ای از ترید یا برنامه‌نویسی ندارید، باز هم بتوانید ابزار را اجرا کنید.

### 1) این ابزار دقیقاً چه کاری انجام می‌دهد؟

بک‌تست یعنی شما «استراتژی خرید و فروش» را روی داده‌های قدیمی بازار طلا امتحان می‌کنید تا ببینید در گذشته سودآور بوده یا نه.

این ابزار:
- یک فایل دیتای قیمت طلا (CSV) می‌گیرد
- یک استراتژی ساده را اجرا می‌کند
- نتیجه را به شما می‌گوید (سرمایه اولیه و نهایی)

### 2) اگر هیچ دیتایی ندارید

این پروژه یک دیتای نمونه دارد و بدون هیچ دیتای اضافی هم اجرا می‌شود.

### 3) نصب و اجرا (خیلی ساده)

اگر Termux دارید:
```bash
pkg update -y
pkg install -y python
```

و بعد:
```bash
cd ~/gold_backtest
python -m pip install --upgrade pip
pip install -r requirements.txt
```

حالا اجرا:
```bash
python run.py --data data/xauusd_sample.csv
```

اگر خروجی مثل زیر دیدید یعنی درست اجرا شده:
```
Starting Portfolio Value: 10000.00
Final Portfolio Value: 10000.xx
```

### 4) اگر می‌خواهید با دیتای خودتان اجرا کنید

فایل دیتای خودتان را داخل پوشه `data/` بگذارید و بعد این دستور را بزنید:
```bash
python run.py --data data/xauusd.csv
```

### 5) اگر دیتای شما تاریخ و ساعت دارد

مثلاً تاریخ به این شکل است: `2024-01-02 14:30:00`

این دستور را اجرا کنید:
```bash
python run.py --data data/xauusd.csv --dtformat "%Y-%m-%d %H:%M:%S"
```

### 6) اگر برنامه ارور داد چه کار کنم؟

بیشتر خطاها به خاطر «فرمت اشتباه CSV» یا «کم بودن تعداد داده‌ها» است.

- مطمئن شوید ستون‌ها دقیقاً این ترتیب را دارند:
```
Date,Open,High,Low,Close,Volume,OpenInterest
```
- اگر حجم و اوپن‌اینترست ندارید، مقدار `0` بگذارید.
- اگر دیتای شما خیلی کم است، ابزار خودش دوره‌ها را کوچک می‌کند تا اجرا شود.

### 7) ساده‌ترین حالت استفاده (بدون دردسر)

فقط این دستور را استفاده کنید:
```bash
python run.py --strategy sma_cross
```

همین، کافی است.

## ویژگی‌ها

- اجرای آسان روی Termux
- پشتیبانی از اکثر آپشن‌های رایج Backtrader (کمیسیون، اسلیپیج، تایم‌فریم، فشرده‌سازی، سizer و ...)
- استراتژی‌های آماده (SMA Cross و RSI Mean Reversion)
- خروجی آنالایزرها (بازده، دراوداون، شارپ، آمار معاملات)
- پشتیبانی از فرمت‌های مختلف CSV با ستون‌بندی قابل تنظیم
- حالت‌های پیشرفته: Renko و Multi-Data

## نصب و اجرا روی Termux

1) نصب پایتون:
```bash
pkg update -y
pkg install -y python
```

2) ورود به پروژه:
```bash
cd ~/gold_backtest
```

3) نصب وابستگی‌ها:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4) اجرای بک‌تست با دیتای نمونه:
```bash
python run.py --data data/xauusd_sample.csv
```

5) مشاهده همه گزینه‌ها:
```bash
python run.py --help
```

### نصب قابلیت رسم نمودار (Plot)

اگر می‌خواهید با `--plot` نمودار ببینید، باید Matplotlib نصب شود:
```bash
pip install matplotlib
```

## فرمت دیتای CSV

پیش‌فرض پروژه این هدر را انتظار دارد:
```
Date,Open,High,Low,Close,Volume,OpenInterest
```

- تاریخ: `YYYY-MM-DD`
- اگر حجم یا اوپن‌اینترست ندارید، مقدار `0` بگذارید.

نمونه:
```
2024-01-02,2042.10,2051.80,2036.40,2048.60,0,0
```
اگر دیتای شما کوتاه باشد و دوره‌های اندیکاتورها بزرگ باشند، ابزار به‌صورت خودکار دوره‌ها را کوچک می‌کند تا خطا ندهد.

### اگر ستون‌هایتان ترتیب متفاوتی دارد

می‌توانید اندیس ستون‌ها را با این پارامترها تنظیم کنید (اندیس از صفر شروع می‌شود):
- `--datecol`، `--opencol`، `--highcol`، `--lowcol`، `--closecol`
- `--volumecol`، `--openinterestcol`

اگر ستونی ندارید مقدار `-1` بدهید.

مثال:
```bash
python run.py --data data/xauusd.csv --datecol 0 --opencol 1 --highcol 2 --lowcol 3 --closecol 4 --volumecol -1 --openinterestcol -1
```

## استراتژی‌ها

### 1) SMA Cross
وقتی میانگین کوتاه از بلند بالاتر می‌رود خرید می‌کند و بالعکس خارج می‌شود.

پارامترها:
- `--fast` (پیش‌فرض 10)
- `--slow` (پیش‌فرض 30)

### 2) RSI Mean Reversion
وقتی RSI پایین می‌رود خرید می‌کند و در محدوده بالا خارج می‌شود.

پارامترها:
- `--rsi-period` (پیش‌فرض 14)
- `--rsi-lower` (پیش‌فرض 30)
- `--rsi-upper` (پیش‌فرض 70)

انتخاب استراتژی:
```bash
python run.py --strategy sma_cross
python run.py --strategy rsi_revert
```

## کنترل ریسک و اندازه پوزیشن (Sizer)

- سایز ثابت:
```bash
python run.py --sizer fixed --stake 1
```

- سایز درصدی از سرمایه:
```bash
python run.py --sizer percent --stake-percent 10
```

## کمیسیون و اسلیپیج

- کمیسیون:
```bash
python run.py --commission 0.0002
```

- اسلیپیج ثابت:
```bash
python run.py --slippage-fixed 0.5
```

- اسلیپیج درصدی:
```bash
python run.py --slippage-perc 0.001
```

## تایم‌فریم و فشرده‌سازی

مثال: دیتای دقیقه‌ای با فشرده‌سازی 5 (هر کندل = 5 دقیقه):
```bash
python run.py --timeframe minutes --compression 5
```

گزینه‌های `--timeframe`:
`ticks` `seconds` `minutes` `days` `weeks` `months` `years`

## محدود کردن بازه زمانی

```bash
python run.py --fromdate 2024-01-01 --todate 2024-06-30
```

## آنالایزرها (خروجی آمار)

```bash
python run.py --analyzers
```

خروجی شامل:
- Max Drawdown
- Sharpe Ratio
- Total Return و Annual Return
- آمار معاملات

## اجرای با Cheat-On-Close یا Cheat-On-Open

```bash
python run.py --coc
python run.py --coo
```

## لیست همه گزینه‌ها

برای دیدن تمام آپشن‌ها:
```bash
python run.py --help
```

## رسم نمودار

```bash
python run.py --plot
```

## مثال‌های آماده

- بک‌تست سریع با SMA:
```bash
python run.py --strategy sma_cross --fast 10 --slow 30
```

- بک‌تست با RSI و اسلیپیج:
```bash
python run.py --strategy rsi_revert --rsi-period 14 --rsi-lower 30 --rsi-upper 70 --slippage-perc 0.001
```

- دیتای با تاریخ و ساعت:
```bash
python run.py --data data/xauusd.csv --dtformat "%Y-%m-%d %H:%M:%S"
```

## نمونه‌های آماده (Examples)

نمونه‌های کاربردی برای بازار طلا در پوشه `examples/` هستند:

1) Resample تایم‌فریم:
```bash
python examples/resample_gold.py --timeframe weekly --compression 1 --plot
```

2) چندتایم‌فریم + Pivot Point:
```bash
python examples/multi_timeframe_pivot.py --higher weekly --plot
```

3) اسلیپیج روی استراتژی SMA:
```bash
python examples/slippage_gold.py --slippage-perc 0.001 --plot
```

4) انواع کمیسیون:
```bash
python examples/commission_gold.py --commtype perc --commission 0.0002 --plot
```

5) Renko برای طلا:
```bash
python examples/renko_gold.py --brick 5 --plot
```

6) چند دیتافید هم‌زمان:
```bash
python examples/multi_data_gold.py --data ../data/xauusd_sample.csv --data2 ../data/xauusd_sample.csv --plot
```

برای جزئیات بیشتر فایل `examples/README.md` را ببینید.

## استفاده از حالت Renko در run.py

```bash
python run.py --mode renko --renko-brick 5 --strategy sma_cross
```

## استفاده از حالت Multi-Data در run.py

```bash
python run.py --mode multi --data data/xauusd_sample.csv --data2 data/xauusd_sample.csv --fast 10 --slow 30
```

## لایسنس و مالکیت

این پروژه تحت لایسنس MIT منتشر شده است.

مالک و صاحب امتیاز: **Raheem-Ansary**

متن کامل لایسنس را در فایل `LICENSE` ببینید.

## وابستگی‌های شخص ثالث

این پروژه از کتابخانه Backtrader استفاده می‌کند که لایسنس مخصوص به خودش را دارد.

اگر نیاز به شخصی‌سازی یا افزودن استراتژی‌های بیشتر دارید، کافی است فایل `strategies.py` را توسعه بدهید.
