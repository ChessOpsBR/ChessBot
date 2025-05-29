import requests
from collections import defaultdict
from infrastructure.headers import HEADERS

def get_archives(username):
    url = f'https://api.chess.com/pub/player/{username}/games/archives'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('archives', [])
    return []

def get_games(archive_url):
    response = requests.get(archive_url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('games', [])
    return []

def get_all_head_to_head(players):
    stats = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0}))
    for player in players:
        archives = get_archives(player)
        for archive in archives:
            games = get_games(archive)
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
