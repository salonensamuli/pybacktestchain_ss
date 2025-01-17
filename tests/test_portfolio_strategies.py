import pytest
import numpy as np
from pybacktestchain_ss.portfolio_strategies import (
    RiskAverseStrategy,
    MinimumVarianceStrategy,
    MaximumReturnStrategy,
    EqualWeightStrategy,
    EqualRiskStrategy,
    MaximumSharpeStrategy
)

@pytest.fixture
def mock_information_set():
    return {
        "expected_return": np.array([0.05, 0.1, -0.02]),
        "covariance_matrix": np.array([
            [0.01,  0.0002, 0.0003],
            [0.0002, 0.02,  0.0001],
            [0.0003, 0.0001, 0.03]
        ]),
        "companies": np.array(["AAPL", "MSFT", "GOOGL"])
    }

def test_risk_averse_strategy(mock_information_set):
    strategy = RiskAverseStrategy
    portfolio = strategy.optimize_portfolio(mock_information_set)

    # portfolio should be a dict with same tickers as keys
    assert set(portfolio.keys()) == set(mock_information_set["companies"])
    
    # weights should sum to ~1.0 (within a small tolerance)
    sum_weights = sum(portfolio.values())
    assert pytest.approx(sum_weights, 0.01) == 1.0

def test_minimum_variance_strategy(mock_information_set):
    strategy = MinimumVarianceStrategy
    portfolio = strategy.optimize_portfolio(mock_information_set)

    assert set(portfolio.keys()) == set(mock_information_set["companies"])
    sum_weights = sum(portfolio.values())
    assert pytest.approx(sum_weights, 0.01) == 1.0

def test_maximum_return_strategy(mock_information_set):
    strategy = MaximumReturnStrategy
    portfolio = strategy.optimize_portfolio(mock_information_set)
    
    assert set(portfolio.keys()) == set(mock_information_set["companies"])
    # for the maximum return asset, the strategy invests 100% there
    # so only one company should have weight=1, the rest=0
    weights = list(portfolio.values())
    assert sum(weights) == pytest.approx(1.0, 0.01)
    # One weight should be 1, the rest 0
    assert any(w == 1.0 for w in weights)
    assert sum(w for w in weights if w == 1.0) == 1.0

def test_equal_weight_strategy(mock_information_set):
    strategy = EqualWeightStrategy
    portfolio = strategy.optimize_portfolio(mock_information_set)
    
    assert set(portfolio.keys()) == set(mock_information_set["companies"])
    # all weights should be equal
    weights = list(portfolio.values())
    assert len(set(weights)) == 1  # meaning all are the same
    # sum to 1
    assert sum(weights) == pytest.approx(1.0, 0.01)

def test_equal_risk_strategy(mock_information_set):
    strategy = EqualRiskStrategy
    portfolio = strategy.optimize_portfolio(mock_information_set)

    assert set(portfolio.keys()) == set(mock_information_set["companies"])
    sum_weights = sum(portfolio.values())
    # should sum to 1, though it might not be super exact
    assert sum_weights == pytest.approx(1.0, 0.01)

def test_maximum_sharpe_strategy(mock_information_set):
    strategy = MaximumSharpeStrategy
    portfolio = strategy.optimize_portfolio(mock_information_set)  # default risk_free_rate=0

    assert set(portfolio.keys()) == set(mock_information_set["companies"])
    sum_weights = sum(portfolio.values())
    assert sum_weights == pytest.approx(1.0, 0.01)
