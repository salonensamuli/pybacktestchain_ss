# pybacktestchain_ss

This repository contains a Streamlit application for PyBacktestChain (backtesting repository developed by https://jfimbett.github.io), providing a user-friendly interface to run backtests on selected stocks with various portfolio strategies. The original code was improved and the UI was designed by Samuli Salonen for the M203 Python course.

This repository enhances the original repository by:
1) Fixing the problem of not having a portfolio between t=0 and first rebalancing date
2) Introducing a new risk model: ProfitTaking
3) Introducing a new rebalancing: EndOfWeek
4) Introducing new investment strategies: MinimumVariance, MaximumReturn, EqualWeight, EqualRisk, MaximumSharpe
5) Removing the dependencies between Information and Strategy classes (enabling easier strategy creation for future)
6) Creating an easy-to-use user interface to interact with the library

## Installation

```bash
pip install pybacktestchain_ss
```

## Usage

1. Clone this repository (or copy the relevant files to your local environment).
2. Install the necessary dependencies (e.g., streamlit, matplotlib, pandas, numpy, sec_cik_mapper, yfinance). Poetry lock file is included in the repository for quick installations.
3. Navigate to the directory containing this streamlit_app.py file.
4. Run
```bash
streamlit run streamlit_app.py
```
or access directly via https://pybacktestchainss.streamlit.app/

## Step-by-step guide for Streamlit app

1. Choose start/end dates for the backtest
2. Choose stocks from the SEC universe (typing the ticker or selecting from the dropdown)
3. Select initial cash amount
4. Specify a risk model (StopLoss or ProfitTaking) and its threshold
5. Pick a portfolio optimization strategy (risk-averse, min variance, etc.)
6. Run the backtest, then view the final and initial portfolio allocations as pie charts, and a line chart of the portfolio value over time

## Step-by-step guide for regular use

```bash
from pybacktestchain_ss.data_module import FirstTwoMoments
from pybacktestchain_ss.broker import Backtest, StopLoss, ProfitTaking
from pybacktestchain_ss.portfolio_strategies import RiskAverseStrategy, \
    MaximumReturnStrategy, MinimumVarianceStrategy, MaximumSharpeStrategy, EqualRiskStrategy, EqualWeightStrategy
from datetime import datetime, timedelta

# Set verbosity for logging
verbose = False  # Set to True to enable logging, or False to suppress it
backtest = Backtest(
    initial_date=datetime(2019, 1, 1),
    final_date=datetime(2020, 1, 1),
    universe = ['AAPL', 'MSFT', "WMT", "TSLA", "SNAP"],
    initial_cash = 1000000,
    information_class=FirstTwoMoments,
    risk_model=StopLoss,
    risk_threshold=0.1,
    name_blockchain="backtest",
    portfolio_strategy=EqualRiskStrategy,
    s=timedelta(days=360),
    verbose=verbose
)

df, initial_port, final_port = backtest.run_backtest()
df["Portfolio value"].plot();

```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pybacktestchain_ss` was created by Samuli Salonen. It is licensed under the terms of the MIT license.

## Credits

`pybacktestchain_ss` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
