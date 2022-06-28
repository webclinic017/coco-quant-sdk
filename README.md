## Coco Quant SDK

**Coco Quant SDK** is an open-source algortimic trading framework for Python.

## Contents

1. [Installation](#installation)
2. [Quick start](#quick-start)
   - [EOD module](#eod-module)
     - [EOD price data for Apple](#download-eod-price-data-for-apple)
     - [Fundamental data for Apple](#download-fundamental-data-for-apple)
     - [Sentiment data for Apple](#download-sentiment-data-for-apple)
     - [Macro indicator data for USA](#download-macro-indicator-data-for-usa)
     - [Economic evewnts](#download-economic-events)
     - [EOD price data for all listing instruments in NYSE](#download-eod-price-data-for-all-listing-instruments-in-NYSE)


## Installation

```bash
$ pip install -U git+https://github.com/minisoba/coco-quant-sdk.git
```

## Quick Start

### EOD Module

**EOD** module contains a helper class to download various financial data offered by [EOD Historical Data API](https://eodhistoricaldata.com/) and save as a [parquet](https://parquet.apache.org/) file.

Currently, the following data set can be downloaded with the APIs.

- EOD prices
- Fundamental data (Stock, ETF, Mutual Fund, Index)
- Finacial news - [topic list](https://eodhistoricaldata.com/financial-apis/financial-news-api/#List_of_Supported_Tags_for_Financial_News)
- Sentiments
- Macro indicators - [available indicators](https://eodhistoricaldata.com/financial-apis/macroeconomics-data-and-macro-indicators-api/#List_of_Available_Macroeconomics_Indicators)
- Economic events

#### Directory structure for downloaded file
**EOD** downloader saves a parquet file in the following directory structure. A convention of leaf node is a *API-name_sub-node* in the JSON response data.
```bash
<base_dir>
├── economic_events
├── eod_prices
├── financial_news
├── fundamentals
│   └── stock
│       ├── analystratings
│       ├── earnings_annual
│       ├── earnings_history
│       ├── earnings_trend
│       ├── financials_balance_sheet_quarterly
│       ├── financials_balance_sheet_yearly
│       ├── financials_cash_flow_quarterly
│       ├── financials_cash_flow_yearly
│       ├── financials_income_statement_quarterly
│       ├── financials_income_statement_yearly
│       ├── general
│       ├── highlights
│       ├── outstandingshares_annual
│       ├── outstandingshares_quarterly
│       ├── technicals
│       └── valuation
├── macro_indicators
│   └── <country>
└── sentiments
```

EOD Historical Data API is a paid service and offers various subscription plans based on type of data. Please check [this](https://eodhistoricaldata.com/pricing) for further information.

#### Download EOD price data for Apple

```python
import logging
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import coco_quant.eod as coco_eod

logging.basicConfig(level="DEBUG")

# Set API token for EOD Historical Data
api_token = 'YOUR API TOKEN'

eod = coco_eod.EodDataDownloader(base_dir='/tmp/eod_data', api_token=api_token)

symbol = 'AAPL.US'

# Download EOD prices
eod.eod_prices(symbol)

start_date = '2022-01-01'
end_date = '2022-06-30'

df = pd.read_parquet(f"/tmp/eod_data/eod_prices/AAPL.US.parq")
x_values = df.loc[(start_date <= df.date) & (df.date <= end_date)].date
y_values = df.loc[(start_date <= df.date) & (df.date <= end_date)].close

fig, ax = plt.subplots(figsize=(8,3))

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

plt.plot(x_values, y_values)
plt.title('AAPL.US Price')
plt.grid()
plt.show()

```

![](https://github.com/minisoba/coco-quant-sdk/blob/8877138bc16792aa67ce853599da03a557f9147b/doc/AAPL_US_chart.png)

#### Download fundamental data for Apple

```python
import logging
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import coco_quant.eod as coco_eod

logging.basicConfig(level="DEBUG")

# Set API token for EOD Historical Data
api_token = 'YOUR API TOKEN'

eod = coco_eod.EodDataDownloader(base_dir='/tmp/eod_data', api_token=api_token)

symbol = 'AAPL.US'

# Download stock fundamental data
eod.stock_fundamentals(symbol)

start_date = '2018-01-01'
end_date = '2022-06-30'

df = pd.read_parquet(f"/tmp/eod_data/fundamentals/stock/earnings_history/AAPL.US.parq")
x_values = df.loc[(start_date <= df.date) & (df.date <= end_date)].date
y_values = df.loc[(start_date <= df.date) & (df.date <= end_date)].epsactual

fig, ax = plt.subplots(figsize=(8,3))

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%y/%m"))

plt.plot(x_values, y_values)
plt.title('AAPL.US EPS')
plt.grid()
plt.show()

```

![](https://github.com/minisoba/coco-quant-sdk/blob/7576c50ae43fc1c0d912d6b24c8bcfdf913c9d10/doc/AAPL_US_EPS_chart.png)

#### Download sentiment data for Apple

```python
>>> eod.sentiments('AAPL.US')
>>> df = pd.read_parquet('/tmp/eod_data/sentiments/AAPL.US.parq')
>>> df[['date', 'polarity', 'neg', 'neu', 'pos']].head(10)
                         date  polarity    neg    neu    pos
0   2022-06-26T15:00:00+00:00     0.998  0.037  0.807  0.156
1   2022-06-26T13:28:00+00:00     0.000  0.000  1.000  0.000
2   2022-06-26T13:01:00+00:00     0.399  0.050  0.880  0.070
3   2022-06-26T12:21:00+00:00     0.625  0.000  0.846  0.154
4   2022-06-26T11:05:00+00:00     0.511  0.000  0.939  0.061
5   2022-06-26T10:22:00+00:00     0.772  0.000  0.660  0.340
6   2022-06-26T09:56:00+00:00     0.178  0.086  0.805  0.109
7   2022-06-26T09:38:00+00:00     0.919  0.000  0.783  0.217
8   2022-06-25T15:53:00+00:00     0.077  0.057  0.860  0.084
9   2022-06-25T10:32:36+00:00    -0.128  0.128  0.824  0.048
>>> df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 50 entries, 0 to 49
Data columns (total 10 columns):
 #   Column    Non-Null Count  Dtype              
---  ------    --------------  -----              
 0   date      50 non-null     datetime64[ns, UTC]
 1   title     50 non-null     object             
 2   content   50 non-null     object             
 3   link      50 non-null     object             
 4   symbols   50 non-null     object             
 5   tags      50 non-null     object             
 6   polarity  50 non-null     float64            
 7   neg       50 non-null     float64            
 8   neu       50 non-null     float64            
 9   pos       50 non-null     float64            
dtypes: datetime64[ns, UTC](1), float64(4), object(5)
memory usage: 4.0+ KB
```

#### Download macro indicator data for USA

*This API requires the Alpha-3 ISO country code as parameter*

```python
>>> eod.macro_indicators('USA')
>>> df = pd.read_parquet('/tmp/eod_data/macro_indicators/USA/inflation_consumer_prices_annual.parq')
>>> df.head(10)
  CountryCode    CountryName                              Indicator        Date  Period   Value
0         USA  United States  Inflation, consumer prices (annual %)  2020-12-31  Annual  1.2336
1         USA  United States  Inflation, consumer prices (annual %)  2019-12-31  Annual  1.8122
2         USA  United States  Inflation, consumer prices (annual %)  2018-12-31  Annual  2.4426
3         USA  United States  Inflation, consumer prices (annual %)  2017-12-31  Annual  2.1301
4         USA  United States  Inflation, consumer prices (annual %)  2016-12-31  Annual  1.2616
5         USA  United States  Inflation, consumer prices (annual %)  2015-12-31  Annual  0.1186
6         USA  United States  Inflation, consumer prices (annual %)  2014-12-31  Annual  1.6222
7         USA  United States  Inflation, consumer prices (annual %)  2013-12-31  Annual  1.4648
8         USA  United States  Inflation, consumer prices (annual %)  2012-12-31  Annual  2.0693
9         USA  United States  Inflation, consumer prices (annual %)  2011-12-31  Annual  3.1568
```

#### Download economic events

```python
>>> eod.economic_events('2022-03-01', '2022-06-20')
>>> df = pd.read_parquet('/tmp/eod_data/economic_events')
>>> df.head(10)
                          type comparison period country                 date  actual  previous  estimate  change  change_percentage
0  Westpac Consumer Confidence       None     Q2      NZ  2022-06-20 23:00:00   78.70     92.10      90.2   -13.4             14.549
1             Balance of Trade       None    May      SV  2022-06-20 22:00:00 -862.22   -855.32    -759.0    -6.9             -0.807
2              ECB Lane Speech       None   None      EU  2022-06-20 19:30:00     NaN       NaN       NaN     NaN                NaN
3             Balance of Trade       None    May      SV  2022-06-20 17:00:00     NaN   -855.32    -759.0     NaN                NaN
4           ECB Panetta Speech       None   None      EU  2022-06-20 17:00:00     NaN       NaN       NaN     NaN                NaN
5             Balance of Trade       None    May      SV  2022-06-20 16:30:00     NaN   -855.32    -759.0     NaN                NaN
6             Balance of Trade       None    May      SV  2022-06-20 15:30:00     NaN   -855.32    -759.0     NaN                NaN
7         6-Month Bill Auction       None   None      US  2022-06-20 15:30:00     NaN       NaN       NaN     NaN                NaN
8         3-Month Bill Auction       None   None      US  2022-06-20 15:30:00     NaN       NaN       NaN     NaN                NaN
9            Unemployment Rate       None    Apr      SI  2022-06-20 14:30:00    5.90      6.20       6.2    -0.3              4.839
```

#### Download financial news for Apple
```python
>>> eod.financial_news('AAPL.US')
>>> df = pd.read_parquet('/tmp/eod_data/financial_news/AAPL.US.parq')
>>> df[['date', 'title']].head(10)
                        date                                                                                    title
0  2022-06-27T21:09:02+00:00                              Movie studios look to cut production amid supply chain woes
1  2022-06-27T21:00:33+00:00                             Sony's Next Big Thing in Tech Is Helping Honda Take On Tesla
2  2022-06-27T20:15:09+00:00  Markets close with losses, energy and utilities lead, Chinese stocks lean to the upside
3  2022-06-27T18:29:00+00:00                                                   The Best True Wireless Earbuds of 2022
4  2022-06-27T17:25:52+00:00                     Roe overturned, Theranos trial, EPA rights: 3 legal stories to watch
5  2022-06-27T17:02:23+00:00      Wells Fargo Enumerates Several Bottlenecks For PayPal; Reiterates Overweight Rating
6  2022-06-27T16:23:00+00:00             Apple May Have 40 Million Subscribers for Streaming TV Service, Analyst Says
7  2022-06-27T16:12:04+00:00            What the Roe v. Wade ruling means for tech companies and reproductive privacy
8  2022-06-27T15:39:42+00:00           Midterm elections, employer abortion benefits: What to watch in D.C. this week
9  2022-06-27T15:12:00+00:00       Formula 1 Could Secure Lucrative Media Rights Deal. Investors May Be Wanting More.
>>> df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 50 entries, 0 to 49
Data columns (total 10 columns):
 #   Column    Non-Null Count  Dtype              
---  ------    --------------  -----              
 0   date      50 non-null     datetime64[ns, UTC]
 1   title     50 non-null     object             
 2   content   50 non-null     object             
 3   link      50 non-null     object             
 4   symbols   50 non-null     object             
 5   tags      50 non-null     object             
 6   polarity  50 non-null     float64            
 7   neg       50 non-null     float64            
 8   neu       50 non-null     float64            
 9   pos       50 non-null     float64            
dtypes: datetime64[ns, UTC](1), float64(4), object(5)
memory usage: 4.0+ KB
```

#### Download EOD price data for all listing instruments in NYSE

Please check [this]() for the supported exchanges by EOD Historical Data API.

*Currently, the bulk download API doesn't support an incremental update and requires one API call per symbol and the list of symbol is obtained with bulk-eod-prices call.*

```python
import logging
import pandas as pd
import coco_quant.eod as coco_eod

logging.basicConfig(level="DEBUG")

# Set API token for EOD Historical Data
api_token = 'YOUR API TOKEN'

eod = coco_eod.EodDataDownloader(base_dir='/tmp/eod_data', api_token=api_token)

exchange = 'NYSE'

# Download EOD prices
eod.eod_prices_exchange(exchange)

# Load all data under /tmp/eod_data/eod_prices
df = pd.read_parquet('/tmp/eod_data/eod_prices')

```
