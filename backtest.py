### Purpose of the following setup is to create a backtesting engine which can actually check the power of a strategy.

from collections.abc import Mapping
from typing import Callable

import pandas as pd
import numpy as np


def backtest(
    data: pd.DataFrame,
    strategy_fn: Callable[..., Mapping[str, float]],
    start_ind: int = 0,
    end_ind: int = -1,
    **kwargs,
) -> pd.DataFrame:
    data = data.copy()
    n = len(data)

    if end_ind < 0:
        end_ind = n
    if start_ind < 0:
        start_ind = 0
    if start_ind >= end_ind:
        raise ValueError("Start index must be less than end index")
    if start_ind >= n:
        raise ValueError("Start index must be less than the length of the data")
    if end_ind > n:
        raise ValueError("End index must be less than or equal to the length of the data")

    # A daily return needs yesterday's close, so the first bar cannot be marked.
    start_ind = max(start_ind, 1)

    price_cols = data.select_dtypes(include="number").columns
    asset_rets = data[price_cols].pct_change()
    daily = np.full(n, np.nan)

    for pos in range(start_ind, end_ind):
        # History excludes today: decide on data through yesterday, earn today's return.
        positions = strategy_fn(data.iloc[:pos], **kwargs)
        today = asset_rets.iloc[pos]
        daily[pos] = sum(weight * today[asset] for asset, weight in positions.items())

    data["returns"] = daily
    data["cumulative_returns"] = (1 + data["returns"]).cumprod() - 1
    return data
