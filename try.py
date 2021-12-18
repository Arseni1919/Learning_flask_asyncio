
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR, MO

friday = (datetime.now() + relativedelta(weekday=FR(-1)))
monday = (datetime.now() + relativedelta(weekday=MO(-1)))
date_for_name = [monday.day, '.', monday.month, '.', monday.year, '-', friday.day, '.', friday.month, '.', friday.year]

date_for_name = ''.join(str(w) for w in date_for_name)

tickers = ['SPY', 'VOO', 'IVV', 'QQQ', 'DIA', 'AMZN', 'AAPL', 'MSFT',
           'FB', 'GOOG', 'GOOGL', 'NFLX', 'TSLA', 'TLT', 'GOVT', 'IEF',
           'SHY', 'GLD', 'IAU', 'LQD', 'VCIT', 'VCSH', 'IGSB', 'VIXY']


data = yf.download(tickers=tickers, period='5d', interval='1m')
data.to_csv(f"{date_for_name}.csv")

data1 = yf.download(tickers=tickers, period='5d', interval='2m')
data1.to_csv(f"{date_for_name} - 2m.csv")