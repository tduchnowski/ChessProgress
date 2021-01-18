# ChessProgress
command line tool for download, analysis and display of progress in chess

Usage:

  For downloading games from chess.com or lichess.org or both:
	
    python main.py -a download -i [start-date]-[end-date] -cu [chesscom-username] -lu [lichessorg-username]
    (games are stored in games.db file which is an sqlite3 database)
		
  For analysis of games stored in games.db:
	
    python main.py -a analyse -i [start-date]-[end-date]
    (this will analyse all games from specified period of time that were not yet analysed. Analysis is done using stockfish)
		
  For displaying monthly average percentage of top stockfish moves played and 'good' moves:
	
    python main.py -a results -i [start-date]-[end-date]
 
 
Those scripts require Stockfish to be installed as well as those python packeges: requests, python-chess, matplotlib.
