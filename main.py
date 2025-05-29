import json
from helpers.data_loader import load_players
from application.get_rank import get_all_ranks
from application.get_head_to_head import get_all_head_to_head

players = load_players()

output = {
    "chess_com": {
        "players_rank": get_all_ranks(players),
        "head_to_head": get_all_head_to_head(players)
    }
}

with open('data/rank.json', 'w', encoding='utf-8') as file:
    json.dump(output, file, indent=4)
