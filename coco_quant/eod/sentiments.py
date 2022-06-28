# -*- coding: utf-8 -*-

import json
import pandas as pd
from logging import getLogger
from .eod_prices import EodData

logger = getLogger(__name__)


class SentimentsData(EodData):
    def __init__(self, base_dir: str, api_token: str):
        super().__init__(f"{base_dir}/sentiments", api_token, ['parse_sentiment'])

    @staticmethod
    def parse_sentiments(data: pd.DataFrame) -> pd.DataFrame:
        sentiment = None
        for i in range(len(data.sentiment)):
            tmp = pd.DataFrame.from_dict([data.sentiment.iloc[i]])
            sentiment = pd.concat([sentiment, tmp], ignore_index=True) if sentiment is not None else tmp
        data.drop('sentiment', axis=1, inplace=True)
        data['date'] = pd.to_datetime(data['date'])
        return pd.concat([data, sentiment], axis=1)

    def sentiments(self, symbol: str) -> None:
        data = self.request("news", [f"s={symbol}"])
        data = json.loads(data)
        data = pd.DataFrame.from_dict(data)
        data = SentimentsData.parse_sentiments(data)
        self.to_parquet(symbol, data)

    def sentiments_country(self, exchange: str) -> None:
        self.bulk_request(exchange, self.sentiments)
