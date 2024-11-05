import pickle
import streamlit as st
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "e86e12d60b1e44cb977b42e8e6829661"
CLIENT_SECRET = "3fbd79b30ae249758d24f34983b770ec"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        song_link = track["external_urls"]["spotify"]  # Get the Spotify URL for the song
        print(album_cover_url)
        print(song_link)  # Print the Spotify URL for the song
        return album_cover_url, song_link
    else:
        # Handle the case when no track is found
        return "https://i.postimg.cc/0QNxYz4V/social.png", None


def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_links = []  # New list to store song links
    for i in distances[1:6]:
        # Fetch the artist and song details
        artist = music.iloc[i[0]].artist
        song_name = music.iloc[i[0]].song
        # Get the album cover URL and song link
        album_cover_url, song_link = get_song_album_cover_url(song_name, artist)
        # Append the details to the respective lists
        recommended_music_posters.append(album_cover_url)
        recommended_music_names.append(song_name)
        recommended_music_links.append(song_link)

    return recommended_music_names, recommended_music_posters, recommended_music_links


st.header('Music Recommender System')
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

music_list = music['song'].values
selected_movie= st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters, recommended_music_links = recommend(selected_movie)
    cols = st.columns(len(recommended_music_names))
    for i, col in enumerate(cols):
        col.text(recommended_music_names[i])
        col.markdown(f'<a href="{recommended_music_links[i]}" target="_blank"><img src="{recommended_music_posters[i]}" style="max-width:200px; height:auto;"></a>', unsafe_allow_html=True)
