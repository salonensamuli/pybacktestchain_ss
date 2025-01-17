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

def main():
    st.title("PyBacktestChain - User Interface")

    st.markdown(
        """
        **Instructions**  
        1) Set the start and end dates for your backtest  
        2) Select one or more stocks from the drop-down list (includes the whole SEC universe)
        3) Define initial cash value
        4) Select a risk model (StopLoss or ProfitTaking or None)  
        5) Select a risk threshold  
        6) Choose a portfolio strategy (Risk Averse, Equal Weight, etc., OBS: if the strategy fails to converge, Equaly Weight is used as default)  
        7) Press **Run backtest** to execute
        """
    )

    # 1) Start and end date
    st.subheader("1) Backtest date range")
    start_date = st.date_input("Start date", value=datetime(2019, 1, 1))
    end_date = st.date_input("End date", value=datetime(2020, 1, 1))
    if start_date >= end_date:
        st.error("Start date must be strictly before End date")

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
    if risk_model_class is None:
        risk_model = None
    else:
        risk_model = risk_model_class

    # 5) Portfolio Strategy
    st.subheader("6) Portfolio strategy")
    strategy_options = {
        "RiskAverseStrategy (original strategy)": RiskAverseStrategy(),
        "MinimumVarianceStrategy": MinimumVarianceStrategy(),
        "MaximumReturnStrategy": MaximumReturnStrategy(),
        "EqualWeightStrategy": EqualWeightStrategy(),
        "EqualRiskStrategy": EqualRiskStrategy(),
        "MaximumSharpeStrategy": MaximumSharpeStrategy()
    }
    selected_strategy_key = st.selectbox("Select a portfolio strategy", list(strategy_options.keys()))
    selected_strategy = strategy_options[selected_strategy_key]

    # 6) Lookback Window (in days, OBS: THIS MUST BE LARGER THAN THE TIME BETWEEN INITIAL AND END DATES!)
    lookback_days = st.number_input("Lookback window (days)", value=360, min_value=1)
    lookback_timedelta = timedelta(days=lookback_days)

    # button to run the backtest
    if st.button("Run backtest"):
        if start_date >= end_date:
            st.error("Please correct date range before running backtest.")
        elif not selected_tickers:
            st.error("Please select at least one ticker before running backtest.")
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
                    risk_model=risk_model,
                    risk_threshold=risk_threshold,
                    portfolio_strategy=selected_strategy,
                    s=lookback_timedelta,
                    verbose=False,   # or True, if you want verbose logs in the console
                    name_blockchain="backtest_streamlit"
                )
                portfolio_values_df = backtest.run_backtest()
                st.success("Backtest completed! See your console/logs for details.")

                fig, ax = plt.subplots()
                ax.plot(portfolio_values_df["Date"], portfolio_values_df["Portfolio value"], label="Portfolio value", color="green")
                ax.set_title("Portfolio value over backtest")
                ax.set_xlabel("Date")
                ax.set_ylabel("Value")
                ax.legend()
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Backtest failed: {e}")
            
if __name__ == "__main__":
    main()
