def find_oldest_album():
    from file_operations import import_music_library
    music_library = (import_music_library())
    import operator
    album_years = {}
    for music_dictionary in music_library:
        album_years[music_dictionary['album name']] = int(music_dictionary['year'])
    return(min(album_years.items(), key=operator.itemgetter(1))[0])   

def find_youngest_album():
    from file_operations import import_music_library
    music_library = (import_music_library())
    import operator
    album_years = {}
    for music_dictionary in music_library:
        album_years[music_dictionary['album name']] = int(music_dictionary['year'])
    return(max(album_years.items(), key=operator.itemgetter(1))[0])
