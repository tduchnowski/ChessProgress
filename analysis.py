import chess
import chess.pgn
import chess.engine 
from io import StringIO

class Analyser:
    def __init__(self):
        blunder_diff = 0.3
        self.engine = chess.engine.SimpleEngine.popen_uci('/usr/bin/stockfish')
        self.engine.configure({'Threads':4})
        self.time_per_move = 0.1
        self.wdl_model = 'Lichess'

    def analyse_game(self, pgn, color):
        blunders_diff = 0.3
        evaluations = []
        game = chess.pgn.read_game(StringIO(pgn))
        print('Analysing the game...')
        best_moves = 0
        player_turns = 0
        while not game.is_end():
            try:
                info = self.engine.analyse(game.board(), chess.engine.Limit(time=self.time_per_move))
                best_move = str(info['pv'][0])
                evaluations.append(self.get_eval(info['score'], color)) 
                turn = game.turn()
                game = game.variations[0]
                if (turn == True and color == 'White') or (turn == False and color == 'Black'):
                    player_turns += 1
                    if str(game.move) == best_move:
                        best_moves += 1
                #if str(game.move) == best_move:
                #    if color == 'White':
                #        if turn == True:
                #            best_moves += 1
                #    else:
                #        if turn == False:
                #            best_moves += 1
            except Exception as e:
                print(e)
                break
        print(f'Analysis finished.')
        if player_turns == 0:
            return {'evals':[], 'best_moves':0, 'best_moves_percentage':0}
        print({'evals': evaluations, 'best_moves_total':best_moves, 'best_move_percentage':100*best_moves/player_turns}) 
        return {'evals': evaluations, 'best_moves_total':best_moves, 'best_move_percentage':100*best_moves/player_turns} 

    def get_eval(self, score, color):
        if color == 'White':
            return score.white().wdl(model=self.wdl_model).expectation()
        else:
            return score.black().wdl(model=self.wdl_model).expectation()

    def get_best_moves(score):
        pass

    def summarize(self, evaluations, color):
        avg_accuracy = -1
        best_moves = 0
        decent_moves = 0
        blunders = 0
        for diff in eval_diffs:
            pass
