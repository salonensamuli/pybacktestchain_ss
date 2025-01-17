# streamlit_app.py
import streamlit as st
from datetime import datetime
from pybacktestchain_ss.data_module import UNIVERSE_SEC, FirstTwoMoments
from pybacktestchain_ss.broker import Backtest, StopLoss, ProfitTaking
from pybacktestchain_ss.portfolio_strategies import (
    RiskAverseStrategy,
    MinimumVarianceStrategy,
    MaximumReturnStrategy,
    EqualWeightStrategy,
    EqualRiskStrategy,
    MaximumSharpeStrategy
)
from matplotlib import pyplot as plt
from datetime import timedelta

portfolio_values_df = None
initial_portfolio_comp = {}
final_portfolio_comp = {}

# plotting function for portfolio compositions
def plot_portfolio_pie(portfolio_dict, title="Portfolio"):
    labels = list(portfolio_dict.keys())
    sizes = list(portfolio_dict.values())
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.set_title(title)
    st.pyplot(fig)

st.set_page_config(layout="wide")

def main():
    st.title("PyBacktestChain - User interface by Samuli Salonen")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            **Instructions**  
            1) Set the start and end dates for your backtest  
            2) Select one or more stocks from the drop-down list (includes the whole SEC universe)
            3) Define an initial cash value
            4) Select a risk model (StopLoss or ProfitTaking or None) and threshold
            5) Choose a portfolio strategy (if the strategy fails to converge, Equal Weight is used as default)  
            6) Press **Run backtest** to execute
            """
        )
        # 1) Start and end date
        st.subheader("1) Backtest date range")
        start_date = st.date_input("Start date", value=datetime(2019, 1, 1))
        end_date = st.date_input("End date", value=datetime(2020, 1, 1))
        if start_date >= end_date:
            st.error("Start date must be strictly before End date")

    with col2:
        # 2) Universe selection
        st.subheader("2) Select tickers (investment universe)")
        selected_tickers = st.multiselect(
            "Select tickers from the SEC universe",
            options=sorted(UNIVERSE_SEC),
            default=["AAPL", "MSFT", "WMT", "TSLA", "SNAP"]
        )
        if not selected_tickers:
            st.warning("No tickers selected. Please pick at least one.")
        # 3) Initial cash
        st.subheader("3) Initial cash")
        initial_cash = st.number_input("How much cash to start with?", value=1000000, min_value=1, step=1000)
        # 4) Risk Model
        st.subheader("4) Risk model")
        risk_models = {
            "None": None,
            "StopLoss": StopLoss,
            "ProfitTaking": ProfitTaking
        }
        selected_risk_model_key = st.selectbox("Select a risk model", list(risk_models.keys()))
        risk_model_class = risk_models[selected_risk_model_key]  # will be None if "None"   
        risk_threshold = st.number_input(
            "Risk threshold (0.0-1.0)",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.01
        )
        
    with col3:
        # 5) Portfolio Strategy
        st.subheader("5) Portfolio strategy")
        strategy_options = {
            "RiskAverseStrategy (original strategy)": RiskAverseStrategy,
            "MinimumVarianceStrategy": MinimumVarianceStrategy,
            "MaximumReturnStrategy": MaximumReturnStrategy,
            "EqualWeightStrategy": EqualWeightStrategy,
            "EqualRiskStrategy": EqualRiskStrategy,
            "MaximumSharpeStrategy": MaximumSharpeStrategy
        }
        selected_strategy_key = st.selectbox("Select a portfolio strategy", list(strategy_options.keys()))
        selected_strategy = strategy_options[selected_strategy_key]
        # OBS: THIS MUST BE LARGER THAN THE TIME BETWEEN INITIAL AND END DATES!
        lookback_days = st.number_input("Lookback window (days)", value=360, min_value=1)
        lookback_timedelta = timedelta(days=lookback_days)
        # button to run the backtest
        run_button = st.button("Run backtest")
        
    if run_button:
        if start_date >= end_date:
            st.error("Please correct date range before running backtest.")
            return
        elif not selected_tickers:
            st.error("Please select at least one ticker before running backtest.")
            return
        else:
            # create the Backtest instance
            st.info("Launching backtest. This may take a moment...")
            try:
                # build the actual dates in datetime form
                start_dt = datetime(start_date.year, start_date.month, start_date.day)
                end_dt = datetime(end_date.year, end_date.month, end_date.day)
                backtest = Backtest(
                    initial_date=start_dt,
                    final_date=end_dt,
                    universe=selected_tickers,
                    initial_cash=initial_cash,
                    information_class=FirstTwoMoments,
                    risk_model=risk_model_class,
                    risk_threshold=risk_threshold,
                    portfolio_strategy=selected_strategy,
                    s=lookback_timedelta,
                    verbose=False,   # or True, if you want verbose logs in the console
                    name_blockchain="backtest_streamlit"
                )
                portfolio_values_df, initial_portfolio_comp, final_portfolio_comp = backtest.run_backtest()
                st.success("Backtest completed! See console/logs for details.")

                with col1:
                # portfolio value over time plot
                    fig, ax = plt.subplots()
                    ax.plot(portfolio_values_df["Date"], portfolio_values_df["Portfolio value"], label="Portfolio value", color="green")
                    ax.set_title("Portfolio value over backtest")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Value")
                    ax.legend()
                    st.pyplot(fig)
                with col2:
                # portfolio initial composition pie
                    if initial_portfolio_comp:
                        plot_portfolio_pie(initial_portfolio_comp, title="Portfolio at the beginning")
                    else:
                        st.warning("No first portfolio recorded (perhaps was empty).")
                with col3:
                # portfolio final composition pie
                    if final_portfolio_comp:
                        plot_portfolio_pie(final_portfolio_comp, title="Portfolio at the end")
                    else:
                        st.warning("No last portfolio recorded.")
            except Exception as e:
                st.error(f"Backtest failed: {e}")
        
if __name__ == "__main__":
    main()