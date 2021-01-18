import json
import math
import matplotlib.pyplot as plt

def group_by_month(games):
    monthly= {}
    for game in games:
        month = game[1].split(' ')[0][:-3]
        g = json.loads(game[5])
        g['color'] = game[4]
        if month in monthly:
            monthly[month].append(g)
        else:
            monthly[month] = [g]
    return monthly

def show(games):
    monthly_games = group_by_month(games)
    summary = {}
    for month,games in monthly_games.items():
        best_move_avg = sum(game['best_move_percentage'] for game in games if 'best_move_percentage' in game)/len(games)
        total_mistakes = 0
        total_decent = 0
        for game in games:
            mistakes, decent = get_mistakes(game['evals'], game['color'])
            total_mistakes += mistakes
            total_decent += decent
        mistakes_per_game = total_mistakes/len(games)
        decent_per_game = total_decent/len(games)
        summary[month] = {'best_move_average':best_move_avg, 'mistakes_per_game': mistakes_per_game,'decent_per_game':decent_per_game}
    plot_progress(summary)

def get_mistakes(evals, color):
    mistakes = 0
    decent = 0
    turns = 0
    if color == 'White':
        r = range(1,len(evals),2)
    else:
        r = range(2,len(evals),2)
    for i in r:
        if abs(evals[i] - evals[i - 1] > 0.2):
            mistakes += 1
        elif abs(evals[i] - evals[i - 1]) < 0.05:
            decent += 1
        turns += 1
    if not turns: return 0,0
    return 100*mistakes/turns, 100*decent/turns

def plot_progress(stats):
    stats = dict(sorted(stats.items(), key=lambda x: x[0]))
    months = [m for m in stats.keys()]
    best_move_averages = [stat['best_move_average'] for stat in stats.values()]
    decent_moves = [stat['decent_per_game'] for stat in stats.values()]
    plt.scatter(months, decent_moves, label='Decent move percentage per game')
    plt.scatter(months, best_move_averages, label='Best move percentage per game')
    plt.legend()
    plt.show()
