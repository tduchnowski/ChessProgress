import argparse
import json
import analysis
import downloader
import results
import time
from database import ManageDb


def analyse(games):
    print(f'To analyse: {len(games)} games')
    analyser = analysis.Analyser()
    for game in games:
        date = game[1]
        pgn = game[3]
        color = game[4]
        print(f'Game from {date}')
        evaluations = json.dumps(analyser.analyse_game(pgn, color))
        print('Writing to the database')
        db.update_evaluations(date, evaluations)
    analyser.engine.quit()

def download(start_date,end_date, chesscom_username, lichess_username):
    downloader.download_games(start_date, end_date, chesscom_username, lichess_username)


parser = argparse.ArgumentParser()
parser.add_argument('-a',help='action',type=str, choices=['analyse','download','results'])
parser.add_argument('-i',help='program will consider games that took place in this time interval',type=str)
parser.add_argument('-cu',help='chess.com username',type=str)
parser.add_argument('-lu',help='lichess username',type=str)
args = parser.parse_args()
if not (args.a and args.i):
    print('Specify action and interval')
    print('Example: -a download -i 2020.05-2020.08 -cu ChessComUsername -lu LichessUsername')
    quit()

interval = args.i.split('-')
start_date = interval[0]
end_date = interval[1]
db = ManageDb('games.db')
if args.a == 'analyse':
    games = db.get_unanalysed(start_date, end_date)
    analyse(games) 
elif args.a == 'download':
    if not (args.cu or args.lu):
        print('You have to provide chess.com and lichess usernames to download your games')
        print('Example: -a download -i 2020.05-2020.08 -cu YourChessComUsername -lu YourLichessUsername')
        quit()
    download(start_date, end_date, args.cu, args.lu)
else:
    games = db.get_games(start_date, end_date)
    results.show(games)
