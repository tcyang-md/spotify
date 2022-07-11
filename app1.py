from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import string
import time
import json

application = Flask(__name__)

app = application

app.secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
app.config['MY_SESSION'] = 'this session'
TOKEN_INFO = "token_info"

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirectPage')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getData', _external=True))

@app.route('/getData')
def getData():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))


    with open('data.json', 'w', encoding='utf-8') as f: json.dump(sp.current_user_top_tracks(limit=20, offset=0, time_range='long_term'), f, ensure_ascii=False, indent=4)

    f = open('data.json')
    data = json.load(f)

    avg_features = {
        'danceability' : 0,
        'energy' : 0,
        'loudness' : 0,
        'speechiness' : 0,
        'acousticness' : 0,
        'instrumentalness' : 0,
        'valence' : 0,
        'tempo' : 0
    }

    # takes dictionary of song attributes, keeps the ones we are looking for as listed in avg_features
    for song in data['items']:
        SongFeats = sp.audio_features(tracks=song['uri'])[0]
        for attribute in SongFeats:
            if attribute in avg_features:
                avg_features[attribute] = avg_features[attribute] + SongFeats.get(attribute)

    for key in avg_features:
        avg_features[key] = avg_features[key] / len(data['items'])

    f.close()


    with open('data.json', 'w', encoding='utf-8') as f: json.dump(sp.current_user_playlists(limit=50, offset=0), f, ensure_ascii=False, indent=4)

    f = open('data.json')
    data = json.load(f)

    number_playlists = len(data['items'])
    f.close()


    # evaluate personality
    personality = ""

    # extroversion
    if avg_features['danceability'] >= 0.50 and avg_features['instrumentalness'] < 0.5 and (avg_features['loudness'] <= -4 and avg_features['loudness'] >= -10) and (avg_features['tempo'] >= 80 and avg_features['tempo'] <= 140):
        personality += "E"
    else:
        personality += "I"

    # World and Process information
    if avg_features["speechiness"] >= 0.1:
        personality += "N"
    else:
        personality += "S"

    # Decision and Emotional coping
    if avg_features["valence"] <= 0.35 and avg_features["acousticness"] >= 0.70 and avg_features["energy"] < 0.50 and avg_features["danceability"] <= 0.50:
        personality += "F"
    else:
        personality += "T"

    # Work, planning, decision-making
    if number_playlists >= 35:
        personality += "J"
    else:
        personality += "P"

    return personality

def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="054c1c9773644bd69cd9f9bb228afd73",
        client_secret = "22608050e9df444dba31b44a43f4c765",
        redirect_uri = url_for('redirectPage', _external = True),
        scope = "user-library-read user-read-playback-state user-modify-playback-state user-read-recently-played user-top-read")
