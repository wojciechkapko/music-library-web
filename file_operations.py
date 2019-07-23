from mymodels import models as mo


def import_music_library(filename='text_albums_data.txt'):
    # read file and create a list of lists with albums data
    with open(filename) as music_file:
        album_list = [element.split(',') for element in music_file.read().split('\n')]
    album_list.pop()
    # return a list of dicts, 1 dict = 1 album
    return [mo.Album(album[0], album[1], album[2], album[3], album[4], index) for index, album in enumerate(album_list)]
