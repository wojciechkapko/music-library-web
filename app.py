from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from view_album_function import view_album
# from suggest_by_genre import suggestions_by_genre
import spotipy
from spotipy import oauth2
from utils import convert_ms_to_min_sec

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'

SPOTIPY_CLIENT_ID = 'a9580eb24ac1422faf7f73bfc96522c7'
SPOTIPY_CLIENT_SECRET = '14af1b8a0d8649a997631e2759043b79'
SPOTIPY_REDIRECT_URI = 'http://music-app-stage.herokuapp.com/'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)


db = SQLAlchemy(app)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(200), nullable=False)
    album_name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(2000), nullable=True)
    genre = db.Column(db.String(200), nullable=False)


def write_to_db(new_album):
    db.session.add(new_album)
    db.session.commit()


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


def get_albums_from_db():
    return Album.query.order_by(Album.album_name).all()


def filter_by_genre(genre):
    return Album.query.order_by(Album.album_name).filter(Album.genre == genre)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-album', methods=['POST', 'GET'])
def add_album():
    if request.method == "POST":

        album_name = request.form['album_name']
        artist_name = request.form['artist_name']
        genre = request.form['genre']
        new_album = Album(album_name=album_name, artist_name=artist_name, genre=genre)
        if check_spotify_for_image(new_album):
            try:
                write_to_db(new_album)
                return redirect('/albums/all')
            except:
                return 'Error'
        else:
            alert = 'Album not found'
            alert_class = 'danger'
            return render_template('add_album.html', alert=alert, alert_class=alert_class)
    else:
        return render_template('add_album.html')


@app.route('/albums/<genre>')
def display_albums_list(genre):

    if genre == 'all':
        # albums = view_album()
        albums = get_albums_from_db()
    else:
        albums = filter_by_genre(genre)

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


@app.route('/delete/<int:id>')
def delete(id):
    album_to_delete = Album.query.get_or_404(id)

    try:
        db.session.delete(album_to_delete)
        db.session.commit()
        return redirect('/albums/all')
    except:
        return 'Error'


def check_spotify_for_image(album):
    spotify = get_token()
    results = spotify.search(q=f'artist:{album.artist_name} album:{album.album_name}', type='album')
    try:
        album.image = results['albums']['items'][0]['images'][0]['url']
        return True
    except:
        return False


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    album_to_edit = Album.query.get_or_404(id)
    if request.method == "POST":

        album_to_edit.album_name = request.form['album_name']
        album_to_edit.artist_name = request.form['artist_name']
        album_to_edit.genre = request.form['genre']

        if check_spotify_for_image(album_to_edit):
            try:
                db.session.commit()
                return redirect('/album/' + str(id))
            except:
                return 'Error'
        else:
            alert = 'Album not found'
            alert_class = 'danger'
            return render_template('edit_album.html', album=album_to_edit, alert=alert, alert_class=alert_class)

    else:
        return render_template('edit_album.html', album=album_to_edit)



if __name__ == '__main__':
    app.run(debug=True)
