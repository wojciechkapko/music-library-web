def count_albums_by_genre():
    from file_operations import import_music_library
    music_library = (import_music_library())
    album_count_by_genres = {}
    for music_dictionary in music_library:
        if music_dictionary['genre'] not in album_count_by_genres.keys():
            album_count_by_genres[music_dictionary['genre']] = 1
        else:
            album_count_by_genres[music_dictionary['genre']] = int(album_count_by_genres[music_dictionary['genre']]) + 1
    return(album_count_by_genres)