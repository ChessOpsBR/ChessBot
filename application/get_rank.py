from infrastructure.player_stats_api import Api
from application.get_rank_format import ChessStats

def get_all_ratings_summary(players: list) -> list:
    """Get the ratings summary of all the players in the list.

    Args:
        players (list): List of player usernames.

    Returns:
        list: List of player ratings summaries.
    """
    ratings_summary = []
    # Iterate over each player and retrieve their ratings summary
    for player in players:
        # Create instances of Api and ChessStats
        data = Api(player).get_status()
        stats = ChessStats(player, data)
        # Append the ratings summary of the player to the list
        ratings_summary.append(stats.get_ratings_summary())
    # Return the list of ratings summaries
    return ratings_summary