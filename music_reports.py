from file_operations import import_music_library


def convert_time_to_float():
    music_list = import_music_library()
    time_list = []
    for item in music_list:
        time = float(item["album time"].replace(":", "."))
        time_list.append(time)
    return time_list


def get_album_name_list():
    music_list = import_music_library()
    album_name_list = []
    for item in music_list:
        album_name_list.append(item["album name"])
    return album_name_list


def find_by_album(name):
    music_list = import_music_library()
    album_name_found = ()
    for item in music_list:
        if name.lower() in item["album name"].lower():
            album_name_found = album_name_found + (item["album name"],)
    return album_name_found


def find_shortest_longest_album(user_input):
    album_name_list = get_album_name_list()
    time_list = convert_time_to_float()
    # user enters 1 if wants to fins shortest album, 2 if longest
    if user_input == "1":
        return album_name_list[time_list.index(min(time_list, key=float))]
    if user_input == "2":
        return album_name_list[time_list.index(max(time_list, key=float))]


def find_by_time_range(user_input):
    from_input = user_input[0]
    to_input = user_input[1]
    # function needs input to be only an int
    time_list = convert_time_to_float()
    album_name_list = get_album_name_list()
    user_output = ()
    i = 0
    if from_input != "" and to_input != "":
        while i < len(time_list):
            if time_list[i] >= from_input and time_list[i] <= to_input:
                user_output = user_output + (album_name_list[i],)
            i += 1
    elif from_input == "" and to_input != "":
        while i < len(time_list):
            if time_list[i] <= to_input:
                user_output = user_output + (album_name_list[i],)
            i += 1
    elif from_input != "" and to_input == "":
        while i < len(time_list):
            if time_list[i] >= from_input:
                user_output = user_output + (album_name_list[i],)
            i += 1
    elif from_input == "" and to_input == "":
        user_output = tuple(album_name_list)

    if len(user_output) > 0:
        return user_output
    else:
        user_output = ()
        user_output = user_output + ("No albums within the given range",)
        return user_output
