import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import pickle

# Sample data
data = pickle.load(open('book_segmentation_results.pkl', 'rb'))
df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# Create the pie chart figure
fig = px.pie(df, names='Segment', values='count', title='Book Author Segment Distribution')

# Update the title font size and other text properties
fig.update_layout(
    title=dict(
        text='Book Author Segment Distribution',  # You can change the title text
        font=dict(size=24)  # Set title font size
    ),
    # Optionally, you can adjust legend and other fonts
    legend=dict(
        font=dict(size=8)  # Adjust the legend font size
    )
)

# Update the text font size in the pie chart
fig.update_traces(
    textfont=dict(size=12)  # Change pie chart label font size
)

# Layout of the app
app.layout = html.Div([
    dcc.Graph(
        id='pie-chart',
        figure=fig,  # Pass the updated figure to the Graph
        config={'responsive': True},
        style={'width': '100%', 'height': '500px', 'margin': 'auto'}
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

