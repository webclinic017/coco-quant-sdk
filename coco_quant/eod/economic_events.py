# -*- coding: utf-8 -*-

import json
import pandas as pd
from logging import getLogger
from datetime import datetime
from .eod_prices import EodData

logger = getLogger(__name__)


class EconomicEventsData(EodData):
    def __init__(self, base_dir: str, api_token: str):
        super().__init__(f"{base_dir}/economic_events", api_token)

    def economic_events(self, from_: datetime, to_: datetime) -> None:
        data = self.request("economic-events", [f"from={from_}", f"to={to_}"])
        data = json.loads(data)
        data = pd.DataFrame(data)
        self.to_parquet("economic_events", data)
