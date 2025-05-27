import json
from infrastructure.player_stats_api import Api
from application.get_rank import ChessStats


with open('players.txt', 'r', encoding='utf-8') as file:
    players = file.read().splitlines()
    
all_ranks = []

for player in players:
    dados = Api(player).get_status()
    rank = ChessStats(player, dados)
    rank = rank.get_actual_rank()
    all_ranks.append(rank)

    
    with open('rank.json', 'w') as file:
            json.dump(all_ranks, file, indent=4)