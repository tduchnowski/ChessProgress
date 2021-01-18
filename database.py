import sqlite3

class ManageDb:
    def __init__(self,path):
        self.conn = None
        try:
            self.conn = sqlite3.connect(path)
        except Error as e:
            print(e)

    def execute_statement(self, statement, params, error_msg):
        if not self.conn == None:
            c = self.conn.cursor()
            if len(params) > 0:
                c.execute(statement, params)
            else:
                c.execute(statement)
        else:
            print(error_msg)

    def create_games_table(self):
        statement = """ CREATE TABLE IF NOT EXISTS games (
                                        id integer PRIMARY KEY,
                                        date text NOT NULL,
                                        source text NOT NULL,
                                        pgn text NOT NULL,
                                        color text NOT NULL,
                                        evaluations text,
                                        UNIQUE(date)
                                    ); """ 
        self.execute_statement(statement, (), 'Error: could not create a table')
        self.conn.commit()

    def add_game(self,date, source, pgn, color, evaluations = 'None'):
        statement = ' INSERT OR IGNORE INTO games(date, source, pgn, color, evaluations) VALUES(?,?,?,?,?) '
        self.execute_statement(statement, (date, source, pgn, color, evaluations), 'Error: could not add a game to the table')
        self.conn.commit()

    def update_evaluations(self, date, evaluations):
        statement = 'UPDATE games SET evaluations = ? WHERE date = ?'
        self.execute_statement(statement, (evaluations, date), 'Error: could not update the row')
        self.conn.commit()

    def remove_empty_games(self):
        pass

    def get_games(self, start_date, end_date):
        if not self.conn == None:
            statement = 'select * from games'
            c = self.conn.cursor()
            c.execute(statement)
            games = c.fetchall()
            games = filter(lambda game: game[1] > start_date and game[1] < end_date, games)
            return games
        else:
            print('Error: could not update the row')
            return []

    def get_unanalysed(self, start_date, end_date):
        statement = 'select * from games where evaluations = "None"'
        if not self.conn == None:
            c = self.conn.cursor()
            c.execute(statement)
            games = c.fetchall()
            games = filter(lambda game: game[1] > start_date and game[1] < end_date, games)
            return list(games)
        else:
            print('Error: could not execute query')
            return []

