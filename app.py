import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Konfigurasi Spotify API
CLIENT_ID = "432e337bb7004e36afbfaea15f4eb151"
CLIENT_SECRET = "f957c80e9b0a47f389716d8a09f75544"

# Inisialisasi klien Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        # Menampilkan gambar default (placeholder) jika cover tidak ditemukan di Spotify
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    # Mengambil indeks lagu yang dipilih
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_music_names = []
    recommended_music_posters = []
    
    # Mengambil 5 rekomendasi teratas (mengabaikan indeks 0 karena itu adalah lagu itu sendiri)
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        song_name = music.iloc[i[0]].song
        
        # Mendapatkan poster dan nama lagu
        recommended_music_posters.append(get_song_album_cover_url(song_name, artist))
        recommended_music_names.append(song_name)

    return recommended_music_names, recommended_music_posters

st.header('Rekomendasi Musik🎵')

# Mengatur path absolut agar aman dari FileNotFoundError
base_dir = os.path.dirname(os.path.abspath(__file__))
df_path = os.path.join(base_dir, 'df.pkl')
similarity_path = os.path.join(base_dir, 'similarity.pkl')

# Mencoba memuat file pickle dengan penanganan error
try:
    with open(df_path, 'rb') as f:
        music = pickle.load(f)
    with open(similarity_path, 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    st.error("⚠️ File 'df.pkl' atau 'similarity.pkl' tidak ditemukan di direktori yang sama dengan 'app.py'. Silakan jalankan sel terakhir di file Jupyter Notebook Anda terlebih dahulu.")
    st.stop() # Menghentikan eksekusi kode di bawahnya jika file tidak ada

music_list = music['song'].values
selected_song = st.selectbox(
    "Ketik lagu yang anda suka atau klik dropdown untuk mencarinya",
    music_list
)

if st.button('Tampilkan Rekomendasi!'):
    with st.spinner("Memuat rekomendasi dan mencari cover album..."):
        recommended_music_names, recommended_music_posters = recommend(selected_song)
        
    # Menggunakan loop untuk merender 5 kolom secara otomatis dan rapi
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_music_names, recommended_music_posters):
        with col:
            st.text(name)
            st.image(poster)