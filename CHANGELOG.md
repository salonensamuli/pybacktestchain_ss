# CHANGELOG


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
