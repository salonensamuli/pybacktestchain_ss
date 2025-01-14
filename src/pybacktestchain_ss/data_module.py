#%%
import yfinance as yf
import pandas as pd 
from sec_cik_mapper import StockMapper
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging 
from scipy.optimize import minimize
import numpy as np
from typing import Optional, Type, Callable

# Setup logging
logging.basicConfig(level=logging.INFO)

#---------------------------------------------------------
# Constants
#---------------------------------------------------------

UNIVERSE_SEC = list(StockMapper().ticker_to_cik.keys())

#---------------------------------------------------------
# Functions
#---------------------------------------------------------

# function that retrieves historical data on prices for a given stock
def get_stock_data(ticker, start_date, end_date):
    """get_stock_data retrieves historical data on prices for a given stock

    Args:
        ticker (str): The stock ticker
        start_date (str): Start date in the format 'YYYY-MM-DD'
        end_date (str): End date in the format 'YYYY-MM-DD'

    Returns:
        pd.DataFrame: A pandas dataframe with the historical data

    Example:
        df = get_stock_data('AAPL', '2000-01-01', '2020-12-31')
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, auto_adjust=False, actions=False)
    # as dataframe 
    df = pd.DataFrame(data)
    df['ticker'] = ticker
    df.reset_index(inplace=True)
    return df

def get_stocks_data(tickers, start_date, end_date):
    """get_stocks_data retrieves historical data on prices for a list of stocks

    Args:
        tickers (list): List of stock tickers
        start_date (str): Start date in the format 'YYYY-MM-DD'
        end_date (str): End date in the format 'YYYY-MM-DD'

    Returns:
        pd.DataFrame: A pandas dataframe with the historical data

    Example:
        df = get_stocks_data(['AAPL', 'MSFT'], '2000-01-01', '2020-12-31')
    """
    # get the data for each stock
    # try/except to avoid errors when a stock is not found
    dfs = []
    for ticker in tickers:
        try:
            df = get_stock_data(ticker, start_date, end_date)
            # append if not empty
            if not df.empty:
                dfs.append(df)
        except:
            logging.warning(f"Stock {ticker} not found")
    # concatenate all dataframes
    data = pd.concat(dfs)
    return data

# test 
# get_stocks_data(['AAPL', 'MSFT'], '2000-01-01', '2020-12-31')
#---------------------------------------------------------
# Classes 
#---------------------------------------------------------

# Class that represents the data used in the backtest. 
@dataclass
class DataModule:
    data: pd.DataFrame

# Interface for the information set 
@dataclass
class Information:
    s: timedelta = timedelta(days=360) # Time step (rolling window)
    data_module: DataModule = None # Data module
    time_column: str = 'Date'
    company_column: str = 'ticker'
    adj_close_column: str = 'Close'
    portfolio_strategy: Callable = None

    def slice_data(self, t : datetime):

        # Get the data module 
        data = self.data_module.data
        # Get the time step 
        s = self.s

        # Convert both `t` and the data column to timezone-aware, if needed
        if t.tzinfo is not None:
            # If `t` is timezone-aware, make sure data is also timezone-aware
            data[self.time_column] = pd.to_datetime(data[self.time_column]).dt.tz_localize(t.tzinfo.zone, ambiguous='NaT', nonexistent='NaT')
        else:
            # If `t` is timezone-naive, ensure the data is timezone-naive as well
            data[self.time_column] = pd.to_datetime(data[self.time_column]).dt.tz_localize(None)
        
        # Get the data only between t-s and t
        data = data[(data[self.time_column] >= t - s) & (data[self.time_column] < t)]
        return data

    def get_prices(self, t : datetime):
        # gets the prices at which the portfolio will be rebalanced at time t 
        data = self.slice_data(t)
        
        # get the last price for each company
        prices = data.groupby(self.company_column)[self.adj_close_column].last()
        # to dict, ticker as key price as value 
        prices = prices.to_dict()
        return prices

    def compute_information(self, t : datetime):  
        pass

    def portfolio_strategy(self, t : datetime, information_set : dict):
        return self.portfolio_strategy(t, information_set)

    def risk_averse_portfolio(self, t : datetime,  information_set : dict):
        pass
     
    def minimum_variance_portfolio(self, t : datetime,  information_set : dict):
        pass

    def maximum_return_portfolio(self, t : datetime,  information_set : dict):
        pass

    def equal_weight_portfolio(self, t : datetime,  information_set : dict):
        pass

    def equal_risk_portfolio(self, t : datetime,  information_set : dict):
        pass

    def maximum_sharpe_portfolio(self, t : datetime,  information_set : dict):
        pass

@dataclass
class FirstTwoMoments(Information):
    def risk_averse_portfolio(self, t:datetime, information_set):
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

    def minimum_variance_portfolio(self, t:datetime, information_set):
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
        
    def maximum_return_portfolio(self, t:datetime, information_set):
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

    def equal_weight_portfolio(self, t:datetime, information_set):
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

    def equal_risk_portfolio(self, t:datetime, information_set):
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

    def maximum_sharpe_portfolio(self, t:datetime, information_set, risk_free_rate=0.0):
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

    def compute_information(self, t : datetime):
        # Get the data module 
        data = self.slice_data(t)
        # the information set will be a dictionary with the data
        information_set = {}

        # sort data by ticker and date
        data = data.sort_values(by=[self.company_column, self.time_column])

        # expected return per company
        data['return'] =  data.groupby(self.company_column)[self.adj_close_column].pct_change() #.mean()
        
        # expected return by company 
        information_set['expected_return'] = data.groupby(self.company_column)['return'].mean().to_numpy()

        # covariance matrix

        # 1. pivot the data
        data = data.pivot(index=self.time_column, columns=self.company_column, values=self.adj_close_column)
        # drop missing values
        data = data.dropna(axis=0)
        # 2. compute the covariance matrix
        covariance_matrix = data.cov()
        # convert to numpy matrix 
        covariance_matrix = covariance_matrix.to_numpy()
        # add to the information set
        information_set['covariance_matrix'] = covariance_matrix
        information_set['companies'] = data.columns.to_numpy()
        return information_set


