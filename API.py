import pandas as pd

data_updated = {
    "API Name": [
        "Finnhub",
        "Alpha Vantage",
        "Yahoo Finance (via RapidAPI)",
        "IEX Cloud",
        "Quandl (Nasdaq Data Link)",
        "Polygon.io",
        "Twelve Data",
        "Intrinio",
        "Marketstack",
        "Financial Modeling Prep"
    ],
    "Link": [
        "https://finnhub.io/",
        "https://www.alphavantage.co/",
        "https://www.rapidapi.com/apis/yahoo-finance",
        "https://iexcloud.io/",
        "https://www.quandl.com/",
        "https://polygon.io/",
        "https://twelvedata.com/",
        "https://intrinio.com/",
        "https://marketstack.com/",
        "https://financialmodelingprep.com/"
    ],
    "Data": [
        "Real-time stock prices, historical data, news, financial statements.",
        "Real-time and historical stock market data, technical indicators, forex, and cryptocurrencies.",
        "Real-time stock prices, historical data, financial news, market statistics.",
        "Real-time stock prices, historical data, financial reports.",
        "Access to financial, economic, and alternative datasets.",
        "Real-time and historical data, including stocks, forex, and crypto.",
        "Real-time stock market data, including historical data, technical analysis, and forex.",
        "Financial data feeds, including real-time stock prices, fundamental data, and market news.",
        "Real-time stock market data, including historical data, intraday prices, and exchange rates.",
        "Stock market data, including financials, earnings reports, and real-time stock prices."
    ],
    "Free Tier": [
        "Yes, limited requests.",
        "Yes, limited daily API calls.",
        "Yes, limited access.",
        "Yes, limited messages/month.",
        "Limited free datasets.",
        "Limited, with paid upgrade for higher usage.",
        "Yes, limited to 800 requests/day.",
        "Limited, with paid plans for access to more data.",
        "Yes, limited features and usage.",
        "Yes, limited access."
    ],
    "Example": [
        "Use the `quote` endpoint for real-time stock data, e.g., `symbol=AAPL`.",
        "Use `TIME_SERIES_INTRADAY` for real-time stock prices, e.g., `symbol=AAPL`.",
        "Get real-time stock quotes for FAANG companies, e.g., `symbol=AAPL`.",
        "Use the `quote` endpoint for stock prices, e.g., `symbol=AAPL`.",
        "Pull historical stock data by specifying ticker symbols.",
        "Use `v2/aggs/ticker` for real-time stock data, e.g., `symbol=AAPL`.",
        "Retrieve real-time stock quotes for FAANG companies, e.g., `symbol=AAPL`.",
        "Use stock price endpoint for real-time quotes, e.g., `symbol=AAPL`.",
        "Get real-time stock prices for FAANG stocks, e.g., `symbol=AAPL`.",
        "Access stock market data for FAANG companies using stock quote endpoints."
    ],
    "Stock": [
        "AAPL - Apple",
        "AAPL - Apple, AMZN - Amazon, META - Meta (Facebook), NFLX - Netflix, GOOGL - Google",
        "AAPL - Apple, AMZN - Amazon, META - Meta (Facebook), NFLX - Netflix, GOOGL - Google",
        "AAPL - Apple, AMZN - Amazon, META - Meta (Facebook), NFLX - Netflix, GOOGL - Google",
        "AAPL - Apple, AMZN - Amazon, META - Meta (Facebook), NFLX - Netflix, GOOGL - Google",
        "AAPL - Apple, AMZN - Amazon, META - Meta (Facebook), NFLX - Netflix, GOOGL - Google",
        "AAPL - Apple, AMZN - Amazon, META - Meta (Facebook), NFLX - Netflix, GOOGL - Google",
        "AAPL - Apple, AMZN - Amazon, META - Meta (Facebook), NFLX - Netflix, GOOGL - Google",
        "AAPL - Apple, AMZN - Amazon, META - Meta (Facebook), NFLX - Netflix, GOOGL - Google",
        "AAPL - Apple, AMZN - Amazon, META - Meta (Facebook), NFLX - Netflix, GOOGL - Google"
    ]
}

# Creating a DataFrame
df_updated = pd.DataFrame(data_updated)

# Save to Excel file
file_path_updated = "FAANG_Stock_APIs_Updated.xlsx"
df_updated.to_excel(file_path_updated, index=False)

file_path_updated
