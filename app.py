from flask import Flask, render_template
from view_album_function import view_album
from genre_filtering import filter_by_genre
from suggest_by_genre import suggestions_by_genre
import sys
import spotipy
import spotipy.util as util

app = Flask(__name__)


spotify = spotipy.Spotify(auth='BQDb2Cdls7QjQQbYL6kskLogvePKeYwSRO3JTzzIQXTzjDTkUykKENb9KZ2xQuCEEzjI6wuxqrhViaz0k4SRsUoG0tdviNXpG4yACvRmf6alAAuwoYzvvXEE_1Iej5SbP6XMeNp7cGtm')

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
