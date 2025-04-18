import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load dataset
df = pd.read_csv("spotify_dashboard_data.csv")

genres = sorted(df["track_genre"].dropna().unique())

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("🎵 Spotify Music Insights", style={'textAlign': 'center'}),

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
    dcc.Graph(id="energy-vs-danceability")
])

@app.callback(
    Output("popularity-bar", "figure"),
    Input("genre-dropdown", "value")
)
def update_bar_chart(selected_genre):
    dff = df[df["track_genre"] == selected_genre]
    top_artists = dff.groupby("artists")["popularity"].mean().nlargest(10).reset_index()
    return px.bar(top_artists, x="artists", y="popularity", title=f"Top Artists in {selected_genre}")

@app.callback(
    Output("energy-vs-danceability", "figure"),
    Input("genre-dropdown", "value")
)
def update_scatter(selected_genre):
    dff = df[df["track_genre"] == selected_genre]
    return px.scatter(dff, x="danceability", y="energy", size="popularity", hover_name="track_name",
                      title=f"Energy vs. Danceability in {selected_genre}", color="artists")

if __name__ == "__main__":
    app.run_server(debug=True)
