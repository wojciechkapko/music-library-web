#from edit_functions import edit_album
from file_operations import import_music_library


def view_album_by_artist(_):
    music_library = (import_music_library())
    user_artist_name = input('Please enter an artist\'s name: ')
    album_by_given_artist = []
    for music_dictionary in music_library:
        if user_artist_name.lower() in (music_dictionary['artist name']).lower():
            album_found = music_dictionary['album name']
            album_by_given_artist.append(album_found)
        else:
            print('No such artist found')
            break
    return(tuple(album_by_given_artist))


def view_album(id=None):
    music_library = import_music_library()
    if id is None:
        return music_library
    else:
        return music_library[int(id)]

