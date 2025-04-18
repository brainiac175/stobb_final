import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load and clean data
df = pd.read_csv("spotify_dashboard_cleaned.csv")

# Drop rows with critical missing values
df = df.dropna(subset=["track_genre", "artists", "popularity", "energy", "danceability", "track_name"])

# Keep only valid numeric values (optional based on your data quality)
df = df[(df["popularity"] >= 0) & (df["popularity"] <= 100)]

# Unique, sorted genres
genres = sorted(df["track_genre"].unique())

# Initialize app
app = Dash(__name__)
server = app.server  # <-- This is what Render looks for!

app.layout = html.Div([
    html.H1("🎶 Spotify Music Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Genre:"),
        dcc.Dropdown(
            id="genre-dropdown",
            options=[{"label": g, "value": g} for g in genres],
            value=genres[0]
        )
    ], style={"width": "50%", "margin": "auto"}),

    html.Hr(),

    dcc.Graph(id="popularity-bar"),
    dcc.Graph(id="energy-dance-scatter")
])

@app.callback(
    Output("popularity-bar", "figure"),
    Input("genre-dropdown", "value")
)
def update_popularity(selected_genre):
    filtered = df[df["track_genre"] == selected_genre]
    top_artists = (
        filtered.groupby("artists")["popularity"]
        .mean()
        .nlargest(10)
        .reset_index()
    )
    return px.bar(
        top_artists,
        x="artists",
        y="popularity",
        title=f"Top 10 Artists in {selected_genre} (by Avg. Popularity)",
        animation_frame=None,
        labels={"popularity": "Avg Popularity"},
        template="plotly_dark"
    )

@app.callback(
    Output("energy-dance-scatter", "figure"),
    Input("genre-dropdown", "value")
)
def update_scatter(selected_genre):
    filtered = df[df["track_genre"] == selected_genre]
    return px.scatter(
        filtered,
        x="danceability",
        y="energy",
        size="popularity",
        color="artists",
        hover_name="track_name",
        title=f"Energy vs Danceability in {selected_genre}",
        animation_frame=None,
        template="plotly_dark"
    )

# Make sure this is callable for gunicorn
if __name__ == "__main__":
    app.run_server(debug=True)




