# -*- coding: utf-8 -*-

import json
import pandas as pd
from logging import getLogger
from .eod_prices import EodData, parse_json

logger = getLogger(__name__)


class FundamentalsData(EodData):
    def __init__(self, base_dir: str, api_token: str, symbol_type: str):
        super().__init__(f"{base_dir}/fundamentals/{symbol_type}", api_token, ['fundamentals', 'fundamentals_exchange', 'process_data'])

    def process_data(self, symbol: str, data: dict, key: str, sub_key: str = None, path_: str = None, conv_fn: str = None) -> None:
        data = parse_json(data, key, sub_key)
        if conv_fn is not None:
            data = conv_fn(data)
        path = path_
        if path is None:
            path = f"{key.lower()}_{sub_key.lower()}" if sub_key is not None else key.lower()
        if data is not None:
            self.to_parquet(symbol, data, path)
        else:
            logger.warning(f"{symbol}: no {path} data")

    def general(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "General")

    def fundamentals(self, symbol: str) -> None:
        data = self.request(f"fundamentals/{symbol}")
        data = json.loads(data)
        for name in self.get_methods():
            fn = getattr(self, name)
            fn(symbol, data)

    def fundamentals_exchange(self, exchange: str):
        self.bulk_request(exchange, self.fundamentals)


class StockFundamentalsData(FundamentalsData):
    def __init__(self, base_dir: str, api_token: str):
        super().__init__(base_dir, api_token, "stock")

    def highlights(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "Highlights")

    def valuation(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "Valuation")

    def share_stats(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "ShareStats")

    def technicals(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "Technicals")

    def analyst_ratings(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "AnalystRatings")

    def earnings(self, symbol: str, data: dict) -> None:
        def conv_fn(data: pd.DataFrame):
            for column in data.columns:
                if column in ['date', 'reportdate']:
                    data[column] = pd.to_datetime(data[column])
                elif column not in ['period', 'currency', 'beforeaftermarket']:
                    data[column] = pd.to_numeric(data[column])
            return data

        for sub_key in ["History", "Trend", "Annual"]:
            self.process_data(symbol, data, "Earnings", sub_key, conv_fn = conv_fn)

    def financials(self, symbol: str, data: dict) -> None:
        def conv_fn(data: pd.DataFrame):
            for column in data.columns:
                if column in ['date', 'filing_date']:
                    data[column] = pd.to_datetime(data[column])
                elif column not in ['currency_symbol']:
                    data[column] = pd.to_numeric(data[column])
            return data

        for key in ["Balance_Sheet", "Cash_Flow", "Income_Statement"]:
            for sub_key in ["quarterly", "yearly"]:
                path = f"financials_{key.lower()}_{sub_key.lower()}"
                self.process_data(symbol, data["Financials"], key, sub_key, path, conv_fn)

    def outstanding_shares(self, symbol: str, data: dict) -> None:
        for sub_key in ["annual", "quarterly"]:
            self.process_data(symbol, data, "outstandingShares", sub_key)


class EtfFundamentalsData(FundamentalsData):
    def __init__(self, base_dir: str, api_token: str):
        super().__init__(base_dir, api_token, "etf")

    def technicals(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "Technicals")

    def etf_data(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "ETF_Data")

    def etf_data_asset_allocation(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "ETF_Data", "Asset_Allocation")

    def etf_data_world_regions(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "ETF_Data", "World_Regions")

    def etf_data_sector_weights(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "ETF_Data", "Sector_Weights")

    def etf_data_fixed_income(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "ETF_Data", "Fixed_Income")

    def etf_data_top_10_holdings(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "ETF_Data", "Top_10_Holdings")


class MutualFundFundamentalsData(FundamentalsData):
    def __init__(self, base_dir: str, api_token: str):
        super().__init__(base_dir, api_token, "mutual_fund")

    def mutual_fund_data(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "MutualFund_Data")

    def mutual_fund_data_asset_allocation(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "MutualFund_Data", "Asset_Allocation")

    def mutual_fund_data_value_growth(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "MutualFund_Data", "Value_Growth")

    def mutual_fund_data_top_holdings(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "MutualFund_Data", "Top_Holdings")

    def mutual_fund_data_market_capitalization(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "MutualFund_Data", "Market_Capitalization")

    def mutual_fund_data_sector_weights(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "MutualFund_Data", "Sector_Weights")

    def mutual_fund_data_world_regions(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "MutualFund_Data", "World_Regions")


class IndexFundamentalsData(FundamentalsData):
    def __init__(self, base_dir: str, api_token: str):
        super().__init__(base_dir, api_token, "index")

    def components(self, symbol: str, data: dict) -> None:
        self.process_data(symbol, data, "Components")
