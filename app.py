import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load cleaned dataset
df = pd.read_csv("spotify_dashboard_cleaned.csv")

# Dropdown values
genres = sorted(df["track_genre"].dropna().unique())
years = sorted(df["year"].unique())

# Init app
app = Dash(__name__)
server = app.server  # Required for deployment on Render

# Layout
app.layout = html.Div([
    html.H1("🎧 Spotify Animated Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Choose Genre:"),
        dcc.Dropdown(
            id='genre-dropdown',
            options=[{'label': genre, 'value': genre} for genre in genres],
            value=genres[0]
        )
    ], style={'width': '48%', 'margin': 'auto'}),

    html.Hr(),

    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='animated-scatter')
])

# Callback: Top 10 artists by popularity (animated by year)
@app.callback(
    Output('bar-chart', 'figure'),
    Input('genre-dropdown', 'value')
)
def update_bar_chart(genre):
    filtered = df[df['track_genre'] == genre]
    top_artists = (
        filtered.groupby(['year', 'artists'])['popularity']
        .mean().reset_index()
        .sort_values(by=['year', 'popularity'], ascending=[True, False])
    )
    top10 = top_artists.groupby("year").head(10)
    fig = px.bar(
        top10,
        x="artists",
        y="popularity",
        color="year",
        barmode="group",
        title="Top 10 Artists by Popularity (Animated by Year)",
        animation_frame="year"
    )
    return fig

# Callback: Danceability vs Energy (animated by year)
@app.callback(
    Output('animated-scatter', 'figure'),
    Input('genre-dropdown', 'value')
)
def update_animated_scatter(genre):
    filtered = df[df['track_genre'] == genre]
    fig = px.scatter(
        filtered,
        x="danceability",
        y="energy",
        size="popularity",
        color="artists",
        hover_name="track_name",
        animation_frame="year",
        range_x=[0, 1],
        range_y=[0, 1],
        title="Danceability vs Energy (Animated by Year)"
    )
    return fig

# Run server
if __name__ == "__main__":
    app.run_server(debug=True)

