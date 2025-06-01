import os
import json
import time
from api.player_stats_api import Api
from application.get_rank_format import ChessStats

FORCE_REFRESH = False  # Set to True to force update all players

def get_all_ratings_summary(players: list) -> dict:
    """
    Get the ratings summary of all the players in the list, updating only changed or missing entries.

    Args:
        players (list): List of player usernames.

    Returns:
        dict: Dictionary of player ratings summaries.
    """
    # Load existing data if available
    rank_path = 'data/rank.json'
    if os.path.exists(rank_path):
        with open(rank_path, 'r', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    # Ensure structure
    if "chess_com" not in existing_data:
        existing_data["chess_com"] = {}
    if "players_ratings_summary" not in existing_data["chess_com"]:
        existing_data["chess_com"]["players_ratings_summary"] = {}

    updated = False
    now = int(time.time())

    # Update only missing or outdated players
    for player in players:
        if (
            player not in existing_data["chess_com"]["players_ratings_summary"]
            or FORCE_REFRESH
        ):
            data = Api(player).get_status()
            stats = ChessStats(player, data)
            summary = stats.get_ratings_summary()
            existing_data["chess_com"]["players_ratings_summary"][player] = summary
            updated = True

    # Save only if there were updates
    if updated:
        with open(rank_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4)

    return existing_data["chess_com"]["players_ratings_summary"]