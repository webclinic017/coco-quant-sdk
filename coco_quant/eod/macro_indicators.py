# -*- coding: utf-8 -*-

import json
import pandas as pd
from logging import getLogger
from .eod_prices import EodData

logger = getLogger(__name__)


class MacroIndicatorsData(EodData):
    def __init__(self, base_dir: str, api_token: str):
        super().__init__(f"{base_dir}/macro_indicators", api_token, ['macro_indicators_exchange'])

    def macro_indicators_exchange(self, exchange: str) -> None:
        for name in self.get_methods():
            data = self.request(f"macro-indicator/{exchange}", [f"indicator={name}"])
            data = json.loads(data)
            data = pd.DataFrame(data)
            fn = getattr(self, name)
            fn(exchange, data)

    def real_interest_rate(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("real_interest_rate", data, exchange)

    def population_total(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("population_total", data, exchange)

    def population_growth_annual(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("population_growth_annual", data, exchange)

    def inflation_consumer_prices_annual(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("inflation_consumer_prices_annual", data, exchange)

    def consumer_price_index(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("consumer_price_index", data, exchange)

    def gdp_current_usd(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gdp_current_usd", data, exchange)

    def gdp_per_capita_usd(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gdp_per_capita_usd", data, exchange)

    def gdp_growth_annual(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gdp_growth_annual", data, exchange)

    def debt_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gdp_growth_annual", data, exchange)

    def net_trades_goods_services(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("net_trades_goods_services", data, exchange)

    def inflation_gdp_deflator_annual(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("inflation_gdp_deflator_annual", data, exchange)

    def agriculture_value_added_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("agriculture_value_added_percent_gdp", data, exchange)

    def industry_value_added_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("industry_value_added_percent_gdp", data, exchange)

    def services_value_added_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("services_value_added_percent_gdp", data, exchange)

    def exports_of_goods_services_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("exports_of_goods_services_percent_gdp", data, exchange)

    def imports_of_goods_services_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("imports_of_goods_services_percent_gdp", data, exchange)

    def gross_capital_formation_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gross_capital_formation_percent_gdp", data, exchange)

    def gross_capital_formation_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gross_capital_formation_percent_gdp", data, exchange)

    def net_migration(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("net_migration", data, exchange)

    def gni_usd(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gni_usd", data, exchange)

    def gni_per_capita_usd(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gni_per_capita_usd", data, exchange)

    def gni_ppp_usd(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gni_ppp_usd", data, exchange)

    def gni_per_capita_ppp_usd(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gni_per_capita_ppp_usd", data, exchange)

    def income_share_lowest_twenty(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("gni_per_capita_ppp_usd", data, exchange)

    def life_expectancy(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("life_expectancy", data, exchange)

    def fertility_rate(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("fertility_rate", data, exchange)

    def prevalence_hiv_total(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("prevalence_hiv_total", data, exchange)

    def co2_emissions_tons_per_capita(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("co2_emissions_tons_per_capita", data, exchange)

    def surface_area_km(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("surface_area_km", data, exchange)

    def poverty_poverty_lines_percent_population(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("poverty_poverty_lines_percent_population", data, exchange)

    def revenue_excluding_grants_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("revenue_excluding_grants_percent_gdp", data, exchange)

    def cash_surplus_deficit_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("cash_surplus_deficit_percent_gdp", data, exchange)

    def startup_procedures_register(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("startup_procedures_register", data, exchange)

    def market_cap_domestic_companies_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("market_cap_domestic_companies_percent_gdp", data, exchange)

    def mobile_subscriptions_per_hundred(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("mobile_subscriptions_per_hundred", data, exchange)

    def internet_users_per_hundred(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("internet_users_per_hundred", data, exchange)

    def high_technology_exports_percent_total(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("high_technology_exports_percent_total", data, exchange)

    def merchandise_trade_percent_gdp(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("merchandise_trade_percent_gdpl", data, exchange)

    def total_debt_service_percent_gni(self, exchange: str, data: pd.DataFrame) -> None:
        self.to_parquet("total_debt_service_percent_gni", data, exchange)
