# -*- coding: utf-8 -*-

import os
import json
import socket
import pandas as pd
import urllib.request as req
from logging import getLogger
from urllib.error import HTTPError
from http.client import IncompleteRead
from collections import namedtuple
from io import StringIO

KeyValue = namedtuple('KeyValue', ['key', 'value'])

EOD_HISTORICAL_DATA_URL = "https://eodhistoricaldata.com/api"

logger = getLogger(__name__)


def parse_csv(data: str, kv: KeyValue = None) -> pd.DataFrame:
    # remove the last line
    df = pd.read_csv(StringIO(data), sep=',', header=0)[:-1]
    if kv is not None:
        df[kv.key] = kv.value
    df.columns = df.columns.str.lower()
    return df


def parse_json(data: dict, key: str, sub_key: str = None) -> pd.DataFrame:
    if key not in data:
        return
    key, data = (sub_key, data[key]) if sub_key is not None else (key, data)
    if key in data:
        df = None
        data = data[key]
        if sub_key is not None:
            for key in data.keys():
                tmp = pd.DataFrame.from_dict([data[key]])
                df = pd.concat([df, tmp], ignore_index=True) if df is not None else tmp
        else:
            df = pd.DataFrame.from_dict([data])
        df.columns = df.columns.str.lower()
        return df


class EodData:
    def __init__(self, base_dir: str, api_token: str, exclude_list: list = []):
        self.base_dir = base_dir
        self.api_token = api_token
        self.exclude_list = ['base_dir', 'api_token', 'get_methods', 'to_parquet', 'request', 'bulk_request', 'eod_latest_prices', 'exclude_list']
        self.exclude_list = self.exclude_list + exclude_list

    def request(self, path: str, params: list = []) -> str:
        logger.info(f"relative-url:{path}:param:{params}")
        params = "&" + "&".join(params) if len(params) > 0 else ""
        url = f"{EOD_HISTORICAL_DATA_URL}/{path}?api_token={self.api_token}{params}"
        with req.urlopen(url) as ret:
            return ret.read().decode("utf-8")

    def bulk_request(self, exchange: str, fn) -> None:
        for index, row in self.eod_latest_prices(exchange).iterrows():
            symbol = f"{row['code']}.{row['ex']}"
            try:
                fn(symbol)
            except HTTPError as ex:
                logger.error(f"HTTPError: code={ex.code}, symbol={symbol}, reason={ex.reason}")
            except socket.error:
                logger.error(f"socket.error: symbol={symbol}")
            except IncompleteRead:
                logger.error(f"IncompleteRead: symbol={symbol}")
            except json.decoder.JSONDecodeError:
                logger.error(f"json.decoder.JSONDecodeError: symbol={symbol}")

    def eod_latest_prices(self, exchange: str) -> pd.DataFrame:
        data = self.request(f"eod-bulk-last-day/{exchange}")
        return parse_csv(data)

    def to_parquet(self, symbol: str, data: pd.DataFrame, parent_dir: str = "") -> None:
        os.makedirs(f"{self.base_dir}/{parent_dir}", exist_ok=True)
        data.to_parquet(f"{self.base_dir}/{parent_dir}/{symbol}.parq")

    def get_methods(self) -> list:
        # skip the private methods
        return list(filter(lambda x: ('__' not in x) & (x not in self.exclude_list), dir(self)))


class EodPricesData(EodData):
    def __init__(self, base_dir: str, api_token: str):
        super().__init__(base_dir, api_token)
        logger.info(f"base_dir:{self.base_dir}")

    def eod_prices(self, symbol: str) -> None:
        data = self.request(f"eod/{symbol}")
        data = parse_csv(data, KeyValue("symbol", symbol))
        data["date"] = pd.to_datetime(data["date"])
        self.to_parquet(symbol, data, "eod_prices")

    def eod_prices_exchange(self, exchange: str) -> None:
        self.bulk_request(exchange, self.eod_prices)
