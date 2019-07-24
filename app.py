from flask import Flask, render_template
from view_album_function import view_album
from genre_filtering import filter_by_genre
from suggest_by_genre import suggestions_by_genre
import spotipy
import spotipy.util as util

app = Flask(__name__)
scope = 'user-library-read'
token = util.prompt_for_user_token('vesparion',scope,client_id='a9580eb24ac1422faf7f73bfc96522c7',client_secret='14af1b8a0d8649a997631e2759043b79',redirect_uri='http://127.0.0.1:5000/')
spotify = spotipy.Spotify(auth=token)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/albums/<genre>')
def display_albums_list(genre):

    if genre == 'all':
        albums = view_album()
    else:
        albums = filter_by_genre(genre)

    for album in albums:
        results = spotify.search(q=f'artist:{album.artist_name} album:{album.album_name}', type='album')
        try:
            album.image = results['albums']['items'][0]['images'][0]['url']
        except IndexError:
            album.image = None
    return render_template('albums.html', albums=albums, genre=genre)


@app.route('/album/<id>')
def view_single_album(id):
    album = view_album(id)
    results = spotify.search(q=f'artist:{album.artist_name} album:{album.album_name}', type='album')
    try:
        album.image = results['albums']['items'][0]['images'][0]['url']
    except IndexError:
        album.image = None

    suggestions = suggestions_by_genre(album.genre)

    for suggestion in suggestions:
        results = spotify.search(q=f'artist:{suggestion.artist_name} album:{suggestion.album_name}', type='album')
        try:
            suggestion.image = results['albums']['items'][0]['images'][0]['url']
        except IndexError:
            suggestion.image = None
    return render_template('album.html', album=album, suggestions=suggestions)


if __name__ == '__main__':
    app.run()
