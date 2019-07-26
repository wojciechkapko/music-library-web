from flask import Flask, render_template, request, redirect
#from view_album_function import view_album
#from genre_filtering import filter_by_genre
#from suggest_by_genre import suggestions_by_genre
import spotipy
from spotipy import oauth2
from utils import convert_ms_to_min_sec
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
db = SQLAlchemy(app)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(200), nullable=False)
    album_name = db.Column(db.String(200), nullable=False)


def get_albums():
    return Album.query.order_by(Album.album_name).all()


    # genre = db.Column(db.String(200), nullable=True)

    # def __init__(self, artist_name, album_name, year, genre, duration, _id):
    #     self.artist_name = artist_name
    #     self.album_name = album_name
    #     self.year = year
    #     self.genre = genre
    #     self.duration = duration
    #     self.id = _id


SPOTIPY_CLIENT_ID = 'a9580eb24ac1422faf7f73bfc96522c7'
SPOTIPY_CLIENT_SECRET = '14af1b8a0d8649a997631e2759043b79'
SPOTIPY_REDIRECT_URI = 'http://music-app-stage.herokuapp.com/'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)


def get_token():
    access_token = ""
    token_info = sp_oauth.get_cached_token()
    if token_info:
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']
    if access_token:
        spotify = spotipy.Spotify(access_token)
    return spotify


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-album', methods=['POST', 'GET'])
def add_album():
    if request.method == "POST":
        new_album = Album(album_name=request.form['album_name'], artist_name=request.form['artist_name'])
        try:
            db.session.add(new_album)
            db.session.commit()
            return redirect('/add-album')
        except:
            return 'Error'
    else:
        return render_template('add_album.html')


@app.route('/albums/<genre>')
def display_albums_list(genre):
    spotify = get_token()
    if genre == 'all':
        # albums = view_album()
        albums = get_albums()
    else:
        albums = filter_by_genre(genre)

    for album in albums:
        results = spotify.search(q=f'artist:{album.artist_name} album:{album.album_name}', type='album')
        try:
            album.image = results['albums']['items'][0]['images'][0]['url']
            album.genre = 'test'
        except IndexError:
            album.image = 'https://www.foot.com/wp-content/uploads/2017/06/placeholder-square.jpg'
    return render_template('albums.html', albums=albums, genre=genre)


@app.route('/album/<id>')
def view_single_album(id):
    spotify = get_token()
    album = Album.query.get_or_404(id)
    results = spotify.search(q=f'artist:{album.artist_name} album:{album.album_name}', type='album')
    try:
        album.image = results['albums']['items'][0]['images'][0]['url']
        album.spotify_link = results['albums']['items'][0]['external_urls']['spotify']
        album_id = results['albums']['items'][0]['id']
        album.genre = 'test'
        api_request = f'spotify:album:{album_id}'

        tracks = spotify.album(api_request)['tracks']['items']
        for track in tracks:
            for key in track.keys():
                if key == 'duration_ms':
                    track[key] = convert_ms_to_min_sec(track[key])
        album.tracks = tracks
    except IndexError:
        album.image = 'https://www.foot.com/wp-content/uploads/2017/06/placeholder-square.jpg'

    # suggestions = suggestions_by_genre(album.genre)

    # for suggestion in suggestions:
    #     results = spotify.search(q=f'artist:{suggestion.artist_name} album:{suggestion.album_name}', type='album')
    #     try:
    #         suggestion.image = results['albums']['items'][0]['images'][0]['url']
    #     except IndexError:
    #         suggestion.image = 'https://www.foot.com/wp-content/uploads/2017/06/placeholder-square.jpg'
    return render_template('album.html', album=album)


if __name__ == '__main__':
    app.run(debug=True)
