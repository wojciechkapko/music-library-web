# import spotipy
# from spotipy import oauth2
# from bottle import request


def validate_menu_choice(max_options=7):
    while True:
        option = input('\n> ')
        if (option.isnumeric() and int(option) <= max_options and int(option) >= 0) or option.lower() == 'x':
            return option
        else:
            print('Incorrect option')


def convert_ms_to_min_sec(millis):
    seconds = (millis/1000) % 60
    seconds = int(seconds)
    minutes = (millis/(1000*60)) % 60
    minutes = int(minutes)

    return ("%d:%d" % (minutes, seconds))



# SPOTIPY_CLIENT_ID = 'a9580eb24ac1422faf7f73bfc96522c7'
# SPOTIPY_CLIENT_SECRET = '14af1b8a0d8649a997631e2759043b79'
# SPOTIPY_REDIRECT_URI = 'http://music-app-stage.herokuapp.com/'
# SCOPE = 'user-library-read'
# CACHE = '.spotipyoauthcache'

# sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)

# access_token = ""
# token_info = sp_oauth.get_cached_token()
# if token_info:
#     print("Found cached token!")
#     access_token = token_info['access_token']
# else:
#     url = request.url
#     code = sp_oauth.parse_response_code(url)
#     if code:
#         print("Found Spotify auth code in Request URL! Trying to get valid access token...")
#         token_info = sp_oauth.get_access_token(code)
#         access_token = token_info['access_token']
# if access_token:
#     print("Access token available! Trying to get user information...")
#     spotify = spotipy.Spotify(access_token)


# results = spotify.search(q=f'artist:Britney Spears album:Baby one more time', type='album')
# album_id = results['albums']['items'][0]['id']
# api_request = f'spotify:album:{album_id}'
# tracks = spotify.album(api_request)['tracks']['items']
# for element in tracks:
#     # print(element)
#     print(element)