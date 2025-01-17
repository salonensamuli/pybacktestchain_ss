# CHANGELOG


## v0.10.1 (2025-01-17)

### Bug Fixes

- **streamlit**: Making the streamlit app site nicer with more organized structure.
  ([`76592be`](https://github.com/salonensamuli/pybacktestchain_ss/commit/76592be186062c40955aa42fab2f8838c95c5555))


## v0.10.0 (2025-01-17)

### Features

- **streamlit**: Added new plots for portfolio compositions. Also made backtesting code a bit easier
  to read by reducing duplicate coding.
  ([`f5e457c`](https://github.com/salonensamuli/pybacktestchain_ss/commit/f5e457c5b8d508edbf572a6365d81955d0f4973d))


## v0.9.4 (2025-01-17)

### Bug Fixes

- **streamlit**: Fixed the calling of strategies which lead to always equal portfolio.
  ([`3853192`](https://github.com/salonensamuli/pybacktestchain_ss/commit/385319261192750259b963dd438fe6b49fa18f68))


## v0.9.3 (2025-01-17)

### Bug Fixes

- **streamlit**: Fixed again the none selection for risk model.
  ([`53ca284`](https://github.com/salonensamuli/pybacktestchain_ss/commit/53ca284ee7c0647d4307212156746ca3315065ef))


## v0.9.2 (2025-01-17)

### Bug Fixes

- **portfolio_strategies**: Removed self from the functions for them to operate properly. Also
  changed the broker to not initiate new buys if quantity is zero.
  ([`e4beeee`](https://github.com/salonensamuli/pybacktestchain_ss/commit/e4beeeecde0c8118313f40b7f23d87e6be8f3ada))


## v0.9.1 (2025-01-17)

### Bug Fixes

- **data_module**: Fixed the compute_portfolio function.
  ([`7d3d1d1`](https://github.com/salonensamuli/pybacktestchain_ss/commit/7d3d1d1f97448fc1410412cf86841ed357e2c687))


## v0.9.0 (2025-01-17)

### Features

- **broker**: Fixed the problem with the original pybacktestchain that the portfolio did not
  initiate until the first rebalancing date. Now the portfolio starts from day1.
  ([`b8450f9`](https://github.com/salonensamuli/pybacktestchain_ss/commit/b8450f95e4f65ce113baa59454bf8330195fc4d7))


## v0.8.2 (2025-01-17)

### Bug Fixes

- **streamlit**: Fixed the bug that selecting no risk model lead to a crash. Also made lookback
  window mutable to comply with the previous changes as well.
  ([`0e3b361`](https://github.com/salonensamuli/pybacktestchain_ss/commit/0e3b3617e00fa5bd7b04a8d8f32923e01a0aaece))


## v0.8.1 (2025-01-17)

### Bug Fixes

- **broker**: Fixed the broker to download stock price data from -timedelta(s) before the start of
  the backtesting, to make sure that timedelta amount of data is avavailable so that the information
  set is complete right from the start.
  ([`33ac476`](https://github.com/salonensamuli/pybacktestchain_ss/commit/33ac476808863326713f2c5afb9e5870cdecc33f))


## v0.8.0 (2025-01-17)

### Features

- **data_module**: Made the lookback window (s) mutable. This used to be hardcoded as 360, which
  lead to the first portfolio being all NaNs, as it couldnt compute the information set.
  ([`a409b83`](https://github.com/salonensamuli/pybacktestchain_ss/commit/a409b837eec8a4bac25a3d261f650134af5d5067))


## v0.7.2 (2025-01-17)

### Bug Fixes

- **altair**: Switching back to matplotlib as I couldnt make altair work after all..
  ([`2be9e68`](https://github.com/salonensamuli/pybacktestchain_ss/commit/2be9e68122c71d145e4ed5bad627e5706f9883cf))


## v0.7.1 (2025-01-17)

### Bug Fixes

- **altair**: Fixed the identation as chart was outside the try and couldnt access the
  portfolio_values_df.
  ([`9cef3ba`](https://github.com/salonensamuli/pybacktestchain_ss/commit/9cef3bafa2df671f6c152e5129c771a5ad38231b))


## v0.7.0 (2025-01-17)

### Features

- **altair**: Changed from matplotlib to altair as it seems to (according to stackoverflow) work
  better with streamlit. Also added it to poetry.
  ([`b4e38f3`](https://github.com/salonensamuli/pybacktestchain_ss/commit/b4e38f39583025a1c94004915e9b4f2ebdfc3704))


## v0.6.2 (2025-01-16)

### Bug Fixes

- **matplotlib**: Now finally fixed it (hope so).
  ([`1b301b9`](https://github.com/salonensamuli/pybacktestchain_ss/commit/1b301b9bcdb461919e6f634fbb30b64f8a9f0e05))


## v0.6.1 (2025-01-16)

### Bug Fixes

- **matplotlib**: Fixed the importing of matplotlib. Also added it to poetry lock.
  ([`6d23c57`](https://github.com/salonensamuli/pybacktestchain_ss/commit/6d23c573636c0310c85d2375390630800c194975))


## v0.6.0 (2025-01-16)

### Features

- **plotting**: First attempt at implementing portfolio value plotting over time. Also cleaned the
  code a little bit (no changes from these).
  ([`5c8944c`](https://github.com/salonensamuli/pybacktestchain_ss/commit/5c8944c6eaa37fb4a593922ee4c8d8f6bd7728aa))


## v0.5.2 (2025-01-15)

### Bug Fixes

- **imports**: Fixed another problem with the imports where some now renamed strategies had their
  old names and thus leading to importing errors. Also cleaned the code a little bit by removing
  unnecessary imports.
  ([`096fd07`](https://github.com/salonensamuli/pybacktestchain_ss/commit/096fd07a1c85b700f662d15255d807f7105205e3))


## v0.5.1 (2025-01-15)

### Bug Fixes

- **imports**: Fixed some library importing problems (some imports had .file instead of
  pybacktestchain_ss.file) related to the streamlit user interface.
  ([`217cf93`](https://github.com/salonensamuli/pybacktestchain_ss/commit/217cf93c8a7e80450a5ffc57ceadc94c3d0086f5))


## v0.5.0 (2025-01-15)

### Features

- **streamlit**: Removed some unused code and added the first iteration of the streamlit user
  interface code for testing on the streamlit cloud.
  ([`102fa32`](https://github.com/salonensamuli/pybacktestchain_ss/commit/102fa32efed469b261923236c8877dd9e946abbf))


## v0.4.0 (2025-01-14)

### Features

- **portfolio_strategies**: Created a new .py file to make editing and storing different strategies
  more simple. Also detached the strategies from the Information class for easier manipulation. The
  user can now choose which strategy to implement (note: maximum sharpe and equal var strategies
  still have convergence issues).
  ([`31b1729`](https://github.com/salonensamuli/pybacktestchain_ss/commit/31b1729fc54a66c58dd39dfa616eed3b8523ed76))


## v0.3.0 (2025-01-14)

### Features

- **broker**: Added new strategies to the broker, also added a new testing notebook
  ([`6b12a6e`](https://github.com/salonensamuli/pybacktestchain_ss/commit/6b12a6e1f39ab298f872c2227acd18b76475aab1))


## v0.2.0 (2025-01-13)

### Features

- **broker**: Added EndOfWeek class for rebalancing
  ([`bf8d914`](https://github.com/salonensamuli/pybacktestchain_ss/commit/bf8d9141d3ac70c388767ae8cecf9985e2beba5f))


## v0.1.0 (2025-01-13)

### Features

- **broker**: Added ProfitTaking, and made the universe, risk_model, risk_threshold, and
  initial_cash mutable
  ([`f7ee382`](https://github.com/salonensamuli/pybacktestchain_ss/commit/f7ee3822fa02b423de9dc602484fa344f934a838))

- **notebook**: Added a notebook for testing
  ([`3ea2030`](https://github.com/salonensamuli/pybacktestchain_ss/commit/3ea20304b6a9b17fa9e6bba89c9785ec6c93e598))


## v0.0.1 (2025-01-13)

### Bug Fixes

- **poetry**: Fixed poetry dependencies
  ([`da46bda`](https://github.com/salonensamuli/pybacktestchain_ss/commit/da46bdac3870264759a1e1d0fd9e65eb38895644))
