from file_operations import import_music_library


def suggestions_by_genre(genre):
    music_library = import_music_library()
    similar_genres = {
        'ancient': '',
        'hard rock': 'progressive rock,rock',
        'hip hop': '',
        'pop': '',
        'progressive rock': 'rock,hard rock',
        'rock': 'progressive rock,hard rock'
    }

    genres_to_suggest = similar_genres[genre].split(',')
    return [album for album in music_library if album.genre in genres_to_suggest]
