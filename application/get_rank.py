from infrastructure.player_stats_api import Api
from application.get_rank_format import ChessStats

def get_all_ranks(players):
    ranks = []
    for player in players:
        data = Api(player).get_status()
        stats = ChessStats(player, data)
        ranks.append(stats.get_actual_rank())
    return ranks