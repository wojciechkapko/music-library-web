from utils import validate_menu_choice
from music_reports import find_by_album, find_shortest_longest_album, find_by_time_range
from genre_filtering import filter_by_genre
from view_album_function import view_album, view_album_by_artist
import os


def display_logo():
    with open('ascii_logo.txt') as logo_file:
        logo = logo_file.read()
    print(logo)


def display_menu(option='0'):
    running = True
    while running:
        option = menu_options(option)
        if option == 'x':
            running = False


def run_function(parameter=None, function=lambda x: 'Not yet implemented'):
    os.system('clear')
    view_album(function(parameter))
    print('\n0. Go back  x. Exit')


def menu_options(submenu):
    if submenu == '0':
        os.system('clear')
        display_logo()
        options = [
            'View all albums',
            'Filter by genre',
            'Filter by album duration',
            'Display shortest and longest albums',
            'Filter by artist name',
            'Filter by album name',
            'View statistics report'
            ]
        for index, option in enumerate(options):
            print(f'{str(index+1)}. {option}')
        print('x. Exit')
    elif submenu == '1':
        # view all albums
        run_function(function=view_album)
    elif submenu == '2':
        # filter by genre
        run_function(function=filter_by_genre)
    elif submenu == '3':
        # filter by album duration (time range)
        time_range_correct = 0
        while time_range_correct < 2:
            time_range = []
            time_range.append(input('From (minutes): '))
            time_range.append(input('To (minutes): '))
            for index, element in enumerate(time_range):
                if element != '' and element.isdigit():
                    time_range[index] = int(element)
                    time_range_correct += 1
                elif element.isdigit() is not True:
                    print(f'Incorrect input - {element}')
                elif element == '':
                    time_range_correct += 1
        run_function(time_range, find_by_time_range)
    elif submenu == '4':
        # find shortest/longest album
        user_input = input('1. for shortest 2. for longest:  ')
        run_function(user_input, find_shortest_longest_album)
    elif submenu == '5':
        # filter by artist name
        run_function(function=view_album_by_artist)
    elif submenu == '6':
        # filter by album name
        name = input('Search by album name: ')
        run_function(name, find_by_album)
    elif submenu == '7':
        # display full report
        run_function()
    return validate_menu_choice()
