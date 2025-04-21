import requests
import pandas as pd

# Replace with your actual credentials
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
YOUTUBE_API_KEY = ''

artists = [
    'Jorge Ben Jor', 'Djavan', 'Tim Maia', 'Gilberto Gil', 'Caetano Veloso',
    'Chico Buarque', 'Rita Lee', 'Maria Bethânia', 'Gal Costa', 'Milton Nascimento',
    'Novos Baianos', 'Tom Jobim', 'Os Mutantes', 'João Gilberto', 'Elis Regina'
]

def get_spotify_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    response = requests.post(url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    return response.json().get('access_token')

def search_spotify_artist(token, artist_name):
    url = f'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'q': artist_name, 'type': 'artist', 'limit': 1}
    response = requests.get(url, headers=headers, params=params).json()
    items = response.get('artists', {}).get('items', [])
    return items[0]['id'] if items else None

def get_spotify_artist_data(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {'Authorization': f'Bearer {token}'}
    return requests.get(url, headers=headers).json()

def search_youtube_channel(api_key, artist_name):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': artist_name,
        'type': 'channel',
        'key': api_key,
        'maxResults': 1
    }
    response = requests.get(url, params=params).json()
    items = response.get('items', [])
    return items[0]['snippet']['channelId'] if items else None

def get_youtube_channel_stats(api_key, channel_id):
    url = 'https://www.googleapis.com/youtube/v3/channels'
    params = {
        'part': 'statistics',
        'id': channel_id,
        'key': api_key
    }
    response = requests.get(url, params=params).json()
    return response.get('items', [{}])[0].get('statistics', {})

def collect_artist_data():
    spotify_token = get_spotify_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    data = []

    for artist in artists:
        try:
            spotify_id = search_spotify_artist(spotify_token, artist)
            spotify_data = get_spotify_artist_data(spotify_token, spotify_id) if spotify_id else {}

            youtube_id = search_youtube_channel(YOUTUBE_API_KEY, artist)
            youtube_data = get_youtube_channel_stats(YOUTUBE_API_KEY, youtube_id) if youtube_id else {}

            data.append({
                'Artist': artist,
                'Spotify Followers': spotify_data.get('followers', {}).get('total'),
                'Spotify Popularity': spotify_data.get('popularity'),
                'YouTube Views': youtube_data.get('viewCount'),
                'YouTube Subscribers': youtube_data.get('subscriberCount')
            })

        except Exception as e:
            print(f"Error processing {artist}: {e}")

    return pd.DataFrame(data)

# Run and display
if __name__ == '__main__':
    df = collect_artist_data()
    print(df)

    # Save to CSV
    df.to_csv('brazilian_artists_stats.csv', index=False)
    print("\n✅ Data successfully saved to 'brazilian_artists_stats.csv'")