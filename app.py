import os
import zipfile
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# STEP 1: Download dataset from Kaggle
def download_kaggle_data():
    os.environ['KAGGLE_USERNAME'] = 'your_username'
    os.environ['KAGGLE_KEY'] = 'your_api_key'

    if not os.path.exists("data"):
        os.makedirs("data")

    os.system("kaggle datasets download -d maharshipandya/spotify-tracks-dataset -p data")

    # Unzip it
    with zipfile.ZipFile("data/spotify-tracks-dataset.zip", 'r') as zip_ref:
        zip_ref.extractall("data")

download_kaggle_data()

# STEP 2: Load and preprocess
df = pd.read_csv("data/SpotifyTracks.csv")
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df = df.dropna(subset=["artists", "release_date", "popularity"])
df["year"] = df["release_date"].dt.year

grouped = df.groupby(["year", "artists"])["popularity"].mean().reset_index()
grouped_top = grouped.sort_values(["year", "popularity"], ascending=[True, False]).groupby("year").head(10)

# STEP 3: Dash App
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Spotify Top Artists (Kaggle)", style={'textAlign': 'center'}),
    dcc.Graph(
        id='animated-scatter',
        figure=px.scatter(
            grouped_top,
            x='year',
            y='popularity',
            animation_frame='year',
            color='artists',
            hover_name='artists',
            size_max=45,
            title="Artist Popularity Shift Over Time"
        )
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
