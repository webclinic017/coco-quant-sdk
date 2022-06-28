# -*- coding: utf-8 -*-

import json
import pandas as pd
from logging import getLogger
from .eod_prices import EodData
from .sentiments import SentimentsData

logger = getLogger(__name__)


class FinancialNewsData(EodData):
    def __init__(self, base_dir: str, api_token: str):
        super().__init__(f"{base_dir}/financial_news", api_token)

    def financial_news(self, symbol: str) -> None:
        data = self.request("news", [f"s={symbol}"])
        data = json.loads(data)
        data = pd.DataFrame.from_dict(data)
        data = SentimentsData.parse_sentiments(data)
        self.to_parquet(symbol, data)

    def financial_news_exchange(self, exchange: str) -> None:
        self.bulk_request(exchange, self.financial_news)
