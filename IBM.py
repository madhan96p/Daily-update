import requests
import pandas as pd
import plotly.graph_objects as go

api_key = 'F6HKOJBIRWX16IDO'
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}'
r = requests.get(url)
data = r.json()

if 'Time Series (Daily)' in data:
    time_series = data['Time Series (Daily)']
    
    df = pd.DataFrame.from_dict(time_series, orient='index')
    
    df.index = pd.to_datetime(df.index)
    
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    df['Close'] = pd.to_numeric(df['Close'])
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Close'],
        mode='lines+markers',
        name='Close Price',
        
        ))

    fig.update_layout(
        title='IBM Stock Price (Closing)',
        title_x=0.5, 
        xaxis=dict(
            title='Date',
        ),
        yaxis=dict(
            title='Closing Price INR',
            tickprefix="₹",  
            tickformat=",.2f"
        ),
        template='plotly_dark',
        showlegend=True
    )

    fig.show()
else:
    print("Error: Data not found.")
