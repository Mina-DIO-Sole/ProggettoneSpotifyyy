from flask import Blueprint, redirect, request, url_for, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "c1e1e455737c44a5a404101c638179d8"
SPOTIFY_CLIENT_SECRET = "e4d8a63e280e4fe5aa5cb455555c6808"
SPOTIFY_REDIRECT_URI = "https://5000-minadiosole-proggettone-1ulgv8a667m.ws-eu117.gitpod.io/callback" #dopo il login andiamo qui

auth_bp = Blueprint('auth', __name__)

sp_oauth = SpotifyOAuth(
client_id=SPOTIFY_CLIENT_ID,
client_secret=SPOTIFY_CLIENT_SECRET,
redirect_uri=SPOTIFY_REDIRECT_URI,
scope="user-read-private", #permessi x informazioni dell'utente
show_dialog=True #forziamo la richiesta di inserire new credenziali
)

@auth_bp.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url() #login di spotify
    return redirect(auth_url)

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code') #recupero codice di autorizzazione
    token_info = sp_oauth.get_access_token(code) #uso il code per un codice di accesso
    session['token_info'] = token_info #salvo il token nella mia sessione x riutilizzarlo
    return redirect(url_for('home.homepage'))

@auth_bp.route('/logout')
def logout():
    session.clear() #cancelliamo l'access token salvato in session
    return redirect(url_for('auth.login'))

    