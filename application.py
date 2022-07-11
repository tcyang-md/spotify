import random
import string
import time
import json
from flask import Flask, request, url_for, session, redirect, render_template
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configure application
application = Flask(__name__)

app = application

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# set up spotify login variables
app.secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
app.config['MY_SESSION'] = 'this session'
TOKEN_INFO = "token_info"

if __name__ == '__main__':
    app.run()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def index():
    # render template welcome screen
    # html screen has form that brings you to the /login
    #return redirect('/login')
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
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
    return redirect(url_for('getResults', _external=True))

@app.route('/getResults')
def getResults():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    return "done"


# helper methods

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
