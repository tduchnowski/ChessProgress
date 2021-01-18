import requests
import json
import re
from database import ManageDb

def initiate_db():
    db_path = './games.db'
    db = ManageDb(db_path)
    db.create_games_table()
    return db

# download games from a specified website which are more recent than a given date
def download_games(start_date, end_date, chesscom_username, lichess_username):
    # from chess.com
    if not chesscom_username:
        print('Skipping chess.com since no username was provided.')
    else:
        print('Downloading from chess.com...')
        color_expr = f'\[(White|Black) "{chesscom_username}"\]'
        utcdate_expr = '\[UTCDate "(.*)"\]' 
        utctime_expr = '\[UTCTime "(.*)"\]' 
        archives = json.loads(requests.get(api_urls['chess.com'].format(chesscom_username)).content)['archives']
        for month in archives:
            monthly_games = json.loads(requests.get(month).content)['games']
            for game in monthly_games:
                pgn = game['pgn']
                color = re.search(color_expr, pgn).groups(1)[0]
                date = re.search(utcdate_expr, pgn).groups(1)[0]
                time = re.search(utctime_expr, pgn).groups(1)[0]
                db.add_game(f'{date} {time}', "chess.com", pgn, color)
    # from lichess
    if not lichess_username:
        print('Skipping lichess since no username was provided.')
    else:
        # regex is obviusly quite dumb here
        pgn_regex = '(\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\[.*\n\n.*\n\n\n)'
        color_expr = f'\[(White|Black) "{lichess_username}"\]'
        print('Downloading from Lichess...')
        all_games = requests.get(api_urls['lichess'].format(lichess_username)).content.decode('utf-8')
        print('...downloading finished')
        all_games = re.findall(pgn_regex, all_games)
        for pgn in all_games:
            color = re.search(color_expr, pgn).groups(1)[0]
            date = re.search(utcdate_expr, pgn).groups(1)[0]
            time = re.search(utctime_expr, pgn).groups(1)[0]
            db.add_game(f'{date} {time}', "lichess", pgn, color)
    

db = initiate_db()
api_urls = {'chess.com':'https://api.chess.com/pub/player/{}/games/archives',
             'lichess':'https://lichess.org/api/games/user/{}'}
