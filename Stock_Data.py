import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info
from datetime import datetime, timedelta

# Install libraries if not already installed
# !pip install yfinance yahoo_fin pandas

def get_historical_data(tickers, days_back):
    # Get start and end dates
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)

    # Format date for yfinance
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    data_frames = []

    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date_str, end=end_date_str, interval='1h')
            data['Ticker'] = ticker
            data_frames.append(data)
        except Exception as e:
            print(f"Error downloading data for {ticker}: {e}")

    # Combine all data into a single DataFrame
    combined_data = pd.concat(data_frames, axis=0)
    combined_data.reset_index(inplace=True)

    return combined_data


# Get a list of all stock tickers from Yahoo Finance lists
all_ticker_lists = [
    stock_info.tickers_sp500(),    
    stock_info.tickers_dow()    
]

# Combine all tickers into a single list
all_tickers = []
for ticker_list in all_ticker_lists:
    all_tickers.extend(ticker_list)

# Remove duplicates
all_tickers = list(set(all_tickers))

# Set the number of days back you'd like to get data for
days_back = 1

# Get historical data in 1-hour intervals
historical_data = get_historical_data(all_tickers, days_back)

# Save the combined DataFrame to a CSV file
historical_data.to_csv('historical_data.csv', index=False)

