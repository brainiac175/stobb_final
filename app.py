import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load and clean dataset
df = pd.read_csv("spotify_dashboard_cleaned.csv")
df.dropna(subset=["track_genre", "danceability", "energy", "popularity", "track_name", "artists"], inplace=True)
df = df[df["popularity"] > 0]

# Genre dropdown options
genres = sorted(df["track_genre"].unique())

# Setup Dash app
app = Dash(__name__)
server = app.server  # <- This is CRUCIAL for Render

# Layout
app.layout = html.Div([
    html.H1("🎶 Spotify Music Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Genre"),
        dcc.Dropdown(
            id="genre-dropdown",
            options=[{"label": genre, "value": genre} for genre in genres],
            value=genres[0]
        )
    ], style={"width": "50%", "margin": "auto"}),

    html.Hr(),

    dcc.Graph(id="top-artists-bar"),
    dcc.Graph(id="animated-scatter")
])

# Callbacks
@app.callback(
    Output("top-artists-bar", "figure"),
    Input("genre-dropdown", "value")
)
def update_bar_chart(genre):
    top_artists = (
        df[df["track_genre"] == genre]
        .groupby("artists")["popularity"]
        .mean()
        .nlargest(10)
        .reset_index()
    )
    return px.bar(top_artists, x="artists", y="popularity", title=f"Top 10 Artists by Popularity in {genre}")

@app.callback(
    Output("animated-scatter", "figure"),
    Input("genre-dropdown", "value")
)
def update_scatter(genre):
    filtered = df[df["track_genre"] == genre]
    fig = px.scatter(
        filtered,
        x="danceability",
        y="energy",
        animation_frame="popularity",  # Treat popularity like a timeline
        size="popularity",
        hover_name="track_name",
        color="artists",
        title=f"Energy vs. Danceability in {genre} (Animated by Popularity)",
        height=600
    )
    fig.update_layout(transition={'duration': 500})
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)



