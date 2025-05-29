from collections import defaultdict
from infrastructure.chess_api import get_archives, get_games_from_archive

def get_all_head_to_head(players):
    stats = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0}))
    for player in players:
        archives = get_archives(player)
        for archive in archives:
            games = get_games_from_archive(archive)
            for game in games:
                white = game['white']['username'].lower()
                black = game['black']['username'].lower()
                result = game['white']['result'] if white == player else game['black']['result']
                opponent = black if white == player else white
                if opponent in players and opponent != player:
                    if result == 'win':
                        stats[player][opponent]['wins'] += 1
                        stats[opponent][player]['losses'] += 1
                    elif result == 'loss':
                        stats[player][opponent]['losses'] += 1
                        stats[opponent][player]['wins'] += 1
                    elif result in ['agreed', 'repetition', 'stalemate', 'timevsinsufficient']:
                        stats[player][opponent]['draws'] += 1
                        stats[opponent][player]['draws'] += 1
    return {player: dict(opponents) for player, opponents in stats.items()}