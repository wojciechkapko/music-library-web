def edit_album(user_album_name):
    from file_operations import import_music_library
    music_library = import_music_library()

    for element in music_library:
        if element['album name'] == user_album_name:
            album_to_edit = element

    print('What do you want to change?: ')
    i = 1
    for element in album_to_edit.keys():
        print(f'{i}. {element.capitalize()}')
        i += 1


# User has to choose which information needs to be changed
# then we ask the user to input new value for the key that was chosen
