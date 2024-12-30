import requests
import pandas as pd
import plotly.graph_objects as go

# Use your API key
api_key = 'F6HKOJBIRWX16IDO'
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}'
r = requests.get(url)
data = r.json()

if 'Time Series (Daily)' in data:
    time_series = data['Time Series (Daily)']
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(time_series, orient='index')
    
    # Convert the index to datetime format
    df.index = pd.to_datetime(df.index)
    
    # Rename columns for better readability
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    # Convert the 'Close' column to numeric values
    df['Close'] = pd.to_numeric(df['Close'])
    
    # Calculate the max and min closing price for setting Y-axis limits
    y_max = df['Close'].max() * 1.05  # Adding a small margin above max value
    y_min = df['Close'].min() * 0.95  # Adding a small margin below min value

    # Create a figure using Plotly
    fig = go.Figure()

    # Add a trace for closing price
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Close'],
        mode='lines+markers',
        name='Close Price',
        ))

    # Update layout with title, axis labels, and gridlines
    fig.update_layout(
        title='IBM Stock Price (Closing)',
        title_x=0.5,  # Center title
        xaxis=dict(
            title='Date',
            tickangle=45,
            showgrid=True,
            gridwidth=0.5,
            gridcolor='lightgrey'
        ),
        yaxis=dict(
            title='Closing Price (₹)',
            showgrid=True,
            gridwidth=0.5,
            gridcolor='lightgrey',
            tickprefix="₹",  # Add the ₹ symbol
            tickformat=",.2f",  # Format Y-axis to show 2 decimal places
            range=[y_min, y_max]  # Set Y-axis range with added margins
        ),
        template='plotly_dark',  # Dark theme for better aesthetics
        hovermode='closest',  # Hover on points for details
        plot_bgcolor='rgba(0, 0, 0, 0)'  # Transparent background
    )

    # Show the interactive plot
    fig.show()
else:
    print("Error: Data not found.")
