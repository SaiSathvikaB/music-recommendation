import pickle
import faiss
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
    song_to_index = {
    song: idx
    for idx, song in enumerate(music['song'])
}
def recommend(song):

    idx = song_to_index[song]

    query_vector = faiss_index.reconstruct(idx)

    query_vector = query_vector.reshape(1,-1)

    k = 6

    similarities, indices = faiss_index.search(
        query_vector,
        k
    )

    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_links = []

    for rec_idx in indices[0][1:]:

        artist = music.iloc[rec_idx].artist

        song_name = music.iloc[rec_idx].song

        album_cover_url, song_link = (
            get_song_album_cover_url(
                song_name,
                artist
            )
        )

        recommended_music_names.append(
            song_name
        )

        recommended_music_posters.append(
            album_cover_url
        )

        recommended_music_links.append(
            song_link
        )

    return (
        recommended_music_names,
        recommended_music_posters,
        recommended_music_links
    )


    


st.header('Music Recommender System')
music = pickle.load(
    open("df.pkl","rb")
)

faiss_index = faiss.read_index(
    "songs.faiss"
)

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
