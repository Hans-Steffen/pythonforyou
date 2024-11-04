import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# Credenciales de Spotify
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_PLAYLIST_ID = os.getenv('SPOTIFY_PLAYLIST_ID')

# Credenciales de Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Configurar autenticación de Spotify
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Variable para guardar el ID de la última canción
last_track_id = None

def get_last_track():
    results = spotify.playlist_tracks(SPOTIFY_PLAYLIST_ID, limit=1)
    last_track = results['items'][0]['track']
    return last_track['id'], last_track['name'], last_track['artists'][0]['name']

def send_message_to_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

def main():
    global last_track_id
    track_id, track_name, artist_name = get_last_track()
    
    if track_id != last_track_id:
        last_track_id = track_id
        message = f"Nueva canción en la lista de Spotify:\n{track_name} - {artist_name}"
        send_message_to_telegram(message)

if __name__ == "__main__":
    main()
