import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import pickle

# Sample data
data = pickle.load(open('segmentation_results.pkl','rb'))
df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    dcc.Graph(
        id='pie-chart',
        figure=px.pie(df, names='Segment', values='count', title='User Segment Distribution')
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
