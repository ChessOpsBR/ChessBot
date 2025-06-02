import os
import json
from api.player_stats_api import Api
from application.get_rank_format import ChessStats


def get_rank_json(players: list, refresh: bool = False) -> dict:
    """
    Retrieve and update the ratings summary for all players in the provided list.

    This function loads existing player ratings from 'data/rank.json' (if available),
    fetches new data only for players who are missing or whose data needs to be refreshed,
    and then saves the updated ratings summary back to the JSON file.

    Args:
        players (list of str): List of player usernames (should be lowercase).
            Example: ['player1', 'player2', 'player3']
        refresh (bool, optional): If True, forces a refresh of the data for all players,
            even if their data already exists in the JSON file. If False, only missing
            players will be fetched and updated. Default is False.

    Returns:
        dict: Dictionary of player ratings summaries, where each key is a player and the value is their ratings summary.
            Example:
            {
                "player1": {
                    "classic": {...},
                    "blitz": {...},
                    "bullet": {...}
                },
                "player2": {
                    ...
                }
            }
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

    # Update only missing or outdated players
    for player in players:
        if (
            player not in existing_data["chess_com"]["players_ratings_summary"]
            or refresh
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