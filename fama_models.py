
import pandas as pd
import yfinance as yf
import statsmodels.api as sm

def get_fama_french_factors(start, end):
    """ Fetches market, size, value, and momentum factors using ETFs as proxies. """

    # Define market and risk-free rate proxies
    market_ticker = "^GSPC"  # S&P 500 as market proxy
    risk_free_ticker = "^IRX"  # 13-week T-Bill rate as risk-free proxy
    
    # Define factor proxies
    size_ticker = "IWM"  # Russell 2000 ETF (small caps)
    value_ticker = "IVE"  # S&P 500 Value ETF
    growth_ticker = "IVW"  # S&P 500 Growth ETF
    
    # Download data
    market_data = yf.download(market_ticker, start=start, end=end)['Close'].pct_change()

    # If market_data is a DataFrame with a single column, convert it to a Series
    if isinstance(market_data, pd.DataFrame):
        market_data = market_data.iloc[:, 0]  # Extract the first column

    risk_free_data = yf.download(risk_free_ticker, start=start, end=end)['Close'] / 100

    # Ensure `risk_free_data` is a single-column Series
    if isinstance(risk_free_data, pd.DataFrame):
        risk_free_data = risk_free_data.iloc[:, 0]  # Convert to Series

    # Align risk-free rate with market index
    risk_free_data = risk_free_data.reindex(market_data.index, method='ffill')

    # Download factor proxy data
    size_data = yf.download(size_ticker, start=start, end=end)['Close'].pct_change()
    value_data = yf.download(value_ticker, start=start, end=end)['Close'].pct_change()
    growth_data = yf.download(growth_ticker, start=start, end=end)['Close'].pct_change()
    if isinstance(size_data, pd.DataFrame):
        size_data = size_data.iloc[:, 0]   
    if isinstance(value_data, pd.DataFrame):
        value_data = value_data.iloc[:, 0] 
    if isinstance(growth_data, pd.DataFrame):
        growth_data = growth_data.iloc[:, 0]  
    # Create factors DataFrame
    fama_factors = pd.DataFrame(index=market_data.index)
    
    print("Market Data Shape:", value_data.shape)
    print("Risk-Free Data Shape:", growth_data.shape)

    fama_factors['Mkt-RF'] = market_data - risk_free_data  # Market risk premium
    fama_factors['RF'] = risk_free_data  # Risk-free rate
    
    # Size factor (SMB: Small Minus Big)
    fama_factors['SMB'] = size_data - market_data  # Small-cap vs market
    
    # Value factor (HML: High Minus Low)
    fama_factors['HML'] = value_data - growth_data  # Value vs growth
    
    # Momentum factor (UMD: Up Minus Down) - Only for 6-factor model
    rolling_returns = market_data.rolling(window=12).mean().pct_change()
    fama_factors['UMD'] = rolling_returns - rolling_returns.mean()

    # Drop NaN rows
    fama_factors.dropna(inplace=True)
    return fama_factors


def get_stock_data(ticker, start, end):
    """ Fetches stock return data. """
    stock = yf.download(ticker, start=start, end=end)
    
    if stock.empty:
        raise ValueError(f"No data retrieved for {ticker}. Check if the ticker is valid.")
    
    stock['Return'] = stock['Close'].pct_change()
    stock.dropna(inplace=True)
    return stock[['Return']]

 

def run_fama_french_regression(ticker, start, end, model_type="5-factor"):
    """ Runs the Fama-French regression based on user-selected model type. """
    
    stock_returns = get_stock_data(ticker, start, end)
    fama_factors = get_fama_french_factors(start, end)
    
    # Choose factors based on model type
    if model_type == "3-factor":
        ff_factors = fama_factors[['Mkt-RF', 'SMB', 'HML']]
    elif model_type == "5-factor":
        ff_factors = fama_factors[['Mkt-RF', 'SMB', 'HML', 'RF']]
    elif model_type == "6-factor":
        ff_factors = fama_factors[['Mkt-RF', 'SMB', 'HML', 'RF', 'UMD']]
    else:
        raise ValueError("Invalid model type. Choose '3-factor', '5-factor', or '6-factor'.")

 
# Ensure index compatibility before merging
    stock_returns.index = pd.to_datetime(stock_returns.index)
    ff_factors.index = pd.to_datetime(ff_factors.index)

    # Drop MultiIndex levels if they exist in stock_returns
    if isinstance(stock_returns.index, pd.MultiIndex):
        stock_returns = stock_returns.droplevel(0)  # Drop 'Ticker' level, keeping 'Date'

    # Drop MultiIndex levels if they exist in ff_factors
    if isinstance(ff_factors.index, pd.MultiIndex):
        ff_factors = ff_factors.droplevel(0)

    # Align stock_returns with ff_factors before merging
    stock_returns = stock_returns.reindex(ff_factors.index, method='ffill')  # Forward-fill missing dates
      # Drop MultiIndex levels if they exist in stock_returns
    if isinstance(stock_returns.index, pd.MultiIndex):
        stock_returns = stock_returns.reset_index(level=0, drop=True)
 

    # Ensure columns in both DataFrames have a single level
    stock_returns.columns = stock_returns.columns.get_level_values(0)  # Drop extra column levels if they exist
    ff_factors.columns = ff_factors.columns.get_level_values(0)  # Drop any multi-level columns

    # Merge datasets
    data = stock_returns.merge(ff_factors, left_index=True, right_index=True, how='left')
 
    # Check if RF is present
    if 'RF' not in data.columns:
        raise KeyError("Risk-free rate (RF) missing from dataset.")
    
    # Define independent (X) and dependent (Y) variables
    X = data.drop(columns=['Return'])
    X = sm.add_constant(X)
    Y = data['Return'] - data['RF']  # Excess return over risk-free rate

    # Run regression
    model = sm.OLS(Y, X).fit()

    # Display results
    print(f"Regression results for {ticker} using {model_type} model:")
    print(model.summary())
    return model

 
