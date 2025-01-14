from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging 
from scipy.optimize import minimize
import numpy as np


class PortfolioStrategy(ABC):
    """ Abstract base class for any portfolio strategy """
    @abstractmethod
    def optimize_portfolio(self, information_set: dict) -> dict[str, float]:
        pass

@dataclass
class RiskAverseStrategy(PortfolioStrategy):
    def optimize_portfolio(self, information_set):
        try:
            mu = information_set['expected_return']
            Sigma = information_set['covariance_matrix']
            gamma = 1 # risk aversion parameter
            n = len(mu)
            # objective function
            obj = lambda x: -x.dot(mu) + gamma/2 * x.dot(Sigma).dot(x)
            # constraints
            cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            # bounds, allow short selling, +- inf 
            bounds = [(0.0, 1.0)] * n
            # initial guess, equal weights
            x0 = np.ones(n) / n
            # minimize
            res = minimize(obj, x0, constraints=cons, bounds=bounds)

            # prepare dictionary 
            portfolio = {k: None for k in information_set['companies']}

            # if converged update
            if res.success:
                for i, company in enumerate(information_set['companies']):
                    portfolio[company] = res.x[i]
            else:
                raise Exception("Optimization did not converge")

            return portfolio
        except Exception as e:
            # if something goes wrong return an equal weight portfolio but let the user know 
            logging.warning("Error computing Risk Averse Portfolio, returning equal weight portfolio")
            logging.warning(e)
            return {k: 1/len(information_set['companies']) for k in information_set['companies']}

@dataclass
class MinimumVarianceStrategy(PortfolioStrategy):
    def optimize_portfolio(self, information_set):
        """ Finding the minimum variance portfolio which is the vertex of the parabola (closed form solution)"""
        try:
            Sigma = information_set['covariance_matrix']
            n = Sigma.shape[0]
            ones = np.ones(n)
            
            # solve for the weights: w = Σ⁻¹1 / (1ᵀΣ⁻¹1)
            inv_Sigma = np.linalg.inv(Sigma)
            weights = inv_Sigma @ ones / (ones.T @ inv_Sigma @ ones)
            
            portfolio = {company: weights[i] for i, company in enumerate(information_set['companies'])}
            return portfolio
        except Exception as e:
            logging.warning("Error computing Minimum Variance Portfolio, returning equal weight portfolio")
            logging.warning(e)
            return {k: 1/len(information_set['companies']) for k in information_set['companies']}

@dataclass 
class MaximumReturnStrategy(PortfolioStrategy):
    def optimize_portfolio(self, information_set):
        """ Finding the asset with the highest expected return and investing all into that """
        try:
            mu = information_set['expected_return']
            companies = information_set['companies']
            
            # find the index of the maximum return, as this asset will get 100% of the weight
            max_index = np.argmax(mu)
            
            portfolio = {company: 0 for company in companies}
            portfolio[companies[max_index]] = 1.0  # allocate 100% to the max return asset
            return portfolio
        except Exception as e:
            logging.warning("Error computing Maximum Return Portfolio, returning equal weight portfolio")
            logging.warning(e)
            return {k: 1/len(information_set['companies']) for k in information_set['companies']}

@dataclass
class EqualWeightStrategy(PortfolioStrategy):
    def optimize_portfolio(self, information_set):
        """" Classic equally weighted portfolio """
        try:
            companies = information_set['companies']
            n = len(companies)
            # setting equal weights
            portfolio = {company: 1 / n for company in companies}
            return portfolio
        except Exception as e:
            logging.warning("Error computing Equal Weight Portfolio")
            logging.warning(e)
            return {}

@dataclass
class EqualRiskStrategy(PortfolioStrategy):
    def optimize_portfolio(self, information_set):
        """" Weighting each asset so that the risk contributed is equal (also known as risk parity) """
        try:
            Sigma = information_set['covariance_matrix']
            companies = information_set['companies']
            n = len(companies)
            # initially equal weights
            x0 = np.ones(n) / n
            # function to calculate risk contribution of the assets
            def risk_contribution(weights):
                portfolio_variance = weights.T @ Sigma @ weights
                marginal_contributions = Sigma @ weights
                return weights * marginal_contributions / portfolio_variance
            # objective is to minimize the squared deviation of risk contributions
            def objective(weights):
                contributions = risk_contribution(weights)
                equal_contribution = np.ones(n) / n
                return np.sum((contributions - equal_contribution) ** 2)
            constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            bounds = [(0, 1)] * n
            res = minimize(objective, x0, constraints=constraints, bounds=bounds)
            
            if res.success:
                portfolio = {company: res.x[i] for i, company in enumerate(companies)}
            else:
                raise Exception("Optimization did not converge")
            
            return portfolio
        except Exception as e:
            logging.warning("Error computing Equal Risk Portfolio, returning equal weight portfolio")
            logging.warning(e)
            return {k: 1/len(information_set['companies']) for k in information_set['companies']}

@dataclass
class MaximumSharpePortfolio(PortfolioStrategy):
    def optimize_portfolio(self, information_set, risk_free_rate=0.0):
        """ Finding the maximum sharpe portfolio, aka tangency portfolio (with closed form solution) """
        try:
            mu = information_set['expected_return']
            mu_excess = mu - risk_free_rate
            Sigma = information_set['covariance_matrix']
            n = len(mu)
            ones = np.ones(n)
            inv_Sigma = np.linalg.inv(Sigma)
            weights = inv_Sigma @ mu_excess / (ones.T @ inv_Sigma @ mu_excess)
            portfolio = {company: weights[i] for i, company in enumerate(information_set['companies'])}
            return portfolio
        except Exception as e:
            logging.warning("Error computing Maximum Sharpe Portfolio, returning equal weight portfolio")
            logging.warning(e)
            return {k: 1/len(information_set['companies']) for k in information_set['companies']}
