def validate_menu_choice(max_options=7):
    while True:
        option = input('\n> ')
        if (option.isnumeric() and int(option) <= max_options and int(option) >= 0) or option.lower() == 'x':
            return option
        else:
            print('Incorrect option')
