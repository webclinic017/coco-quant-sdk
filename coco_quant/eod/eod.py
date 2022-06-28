# -*- coding: utf-8 -*-

from datetime import datetime
from .eod_prices import EodPricesData
from .sentiments import SentimentsData
from .macro_indicators import MacroIndicatorsData
from .economic_events import EconomicEventsData
from .financial_news import FinancialNewsData
from .fundamentals import StockFundamentalsData, EtfFundamentalsData, MutualFundFundamentalsData, IndexFundamentalsData


class EodDataAPI:
    ETF_FUNDAMENTALS = "etf_fundamentals"
    EOD_PRICES = "eod_prices"
    STOCK_FUNDAMENTALS = "stock_fundamentals"
    INDEX_FUNDAMENTALS = "index_fundamentals"
    MUTUAL_FUND_FUNDAMENTALS = "mutual_fund_fundamentals"
    SENTIMENTS = "sentiments"
    MACRO_INDICATORS = "macro_indicators"
    ECONOMIC_EVENTS = "economic_events"
    FINANCIAL_NEWS = "financial_news"


class EodDataDownloader:
    def __init__(self, base_dir: str, api_token: str):
        self.__feed = {
            EodDataAPI.EOD_PRICES: EodPricesData(base_dir, api_token),
            EodDataAPI.STOCK_FUNDAMENTALS: StockFundamentalsData(base_dir, api_token),
            EodDataAPI.ETF_FUNDAMENTALS: EtfFundamentalsData(base_dir, api_token),
            EodDataAPI.INDEX_FUNDAMENTALS: IndexFundamentalsData(base_dir, api_token),
            EodDataAPI.MUTUAL_FUND_FUNDAMENTALS: MutualFundFundamentalsData(base_dir, api_token),
            EodDataAPI.SENTIMENTS: SentimentsData(base_dir, api_token),
            EodDataAPI.MACRO_INDICATORS: MacroIndicatorsData(base_dir, api_token),
            EodDataAPI.ECONOMIC_EVENTS: EconomicEventsData(base_dir, api_token),
            EodDataAPI.FINANCIAL_NEWS: FinancialNewsData(base_dir, api_token),
        }

    def eod_prices(self, symbol: str) -> None:
        self.__feed[EodDataAPI.EOD_PRICES].eod_prices(symbol)

    def eod_prices_country(self, exchange: str) -> None:
        self.__feed[EodDataAPI.EOD_PRICES].eod_prices_exchange(exchange)

    def stock_fundamentals(self, symbol: str) -> None:
        self.__feed[EodDataAPI.STOCK_FUNDAMENTALS].fundamentals(symbol)

    def stock_fundamentals_exchange(self, exchange: str) -> None:
        self.__feed[EodDataAPI.STOCK_FUNDAMENTALS].fundamentals_exchange(exchange)

    def etf_fundamentals(self, symbol: str) -> None:
        self.__feed[EodDataAPI.ETF_FUNDAMENTALS].fundamentals(symbol)

    def etf_fundamentals_exchange(self, exchange: str) -> None:
        self.__feed[EodDataAPI.ETF_FUNDAMENTALS].fundamentals_exchange(exchange)

    def mutual_fund_fundamentals(self, symbol: str) -> None:
        self.__feed[EodDataAPI.MUTUAL_FUND_FUNDAMENTALS].fundamentals(symbol)

    def mutual_fund_fundamentals_exchange(self, exchange: str) -> None:
        self.__feed[EodDataAPI.MUTUAL_FUND_FUNDAMENTALS].fundamentals_exchange(exchange)

    def index_fundamentals(self, symbol: str) -> None:
        self.__feed[EodDataAPI.INDEX_FUNDAMENTALS].fundamentals(symbol)

    def sentiments(self, symbol: str) -> None:
        self.__feed[EodDataAPI.SENTIMENTS].sentiments(symbol)

    def sentiments_exchange(self, exchange: str) -> None:
        self.__feed[EodDataAPI.SENTIMENTS].sentiments_exchange(exchange)

    def macro_indicators(self, exchange: str) -> None:
        self.__feed[EodDataAPI.MACRO_INDICATORS].macro_indicators_exchange(exchange)

    def economic_events(self, from_: datetime, to_: datetime) -> None:
        self.__feed[EodDataAPI.ECONOMIC_EVENTS].economic_events(from_, to_)

    def financial_news(self, symbol: str) -> None:
        self.__feed[EodDataAPI.FINANCIAL_NEWS].financial_news(symbol)

    def financial_news_exchange(self, exchange: str) -> None:
        self.__feed[EodDataAPI.FINANCIAL_NEWS].financial_news_exchange(exchange)
