from file_operations import import_music_library


def get_all_genres(albums):
    return set([value for element in albums for key, value in element.items() if key == 'genre'])


def filter_by_genre(genre):
    albums = import_music_library()
    return list(filter(lambda x: True if x.genre == genre else False, albums))
