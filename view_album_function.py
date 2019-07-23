from edit_functions import edit_album
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

    # user_answer = input('Do you wish to edit? (Y)es or (N)o : ')
    # while user_answer.lower() not in ['yes', 'no', 'y', 'n']:
    #    print('Incorrect input')
    #    user_answer = input('Do you wish to edit? (Y)es or (N)o : ')
#
    # if user_answer.lower() in ['yes', 'y']:
    #    input_is_correct = False
    #    while input_is_correct is False:
    #        try:
    #            index = int(input('Choose album number to edit: '))-1
    #            user_album_name = album_tuple[index]
    #            if index < 0:
    #                raise ValueError
    #        except IndexError or ValueError:
    #            print('Incorrect input')
    #        else:
    #            input_is_correct = True
#
    #    edit_album(user_album_name)
