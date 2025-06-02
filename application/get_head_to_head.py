import os
import json
from collections import defaultdict
from api.chess_api import get_archives, get_games_from_archive


def get_head_to_head_json(players: list, refresh: bool = False) -> dict:
    """
    Calculate head-to-head statistics between all players in the provided list.

    Args:
        players (list of str): List of player usernames (should be lowercase).
            Example: ['player1', 'player2', 'player3']
        refresh (bool, optional): If True, forces a refresh of the data for all players,
            even if their data already exists in the JSON file. If False, only missing
            players will be fetched and updated. Default is False.

    Returns:
        dict: A nested dictionary where each player maps to their opponents and the win/loss/draw counts.
            Example:
            {
                "player1": {
                    "player2": {"wins": 1, "losses": 2, "draws": 0},
                    "player3": {"wins": 0, "losses": 1, "draws": 1}
                },
                "player2": {
                    "player1": {"wins": 2, "losses": 1, "draws": 0},
                    "player3": {"wins": 1, "losses": 0, "draws": 1}
                }
            }
    """
    # Load existing data if exists
    h2h_path = 'data/head_to_head.json'
    if os.path.exists(h2h_path):
        with open(h2h_path, 'r', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}
    
    # Ensure the structure for chess_com and head_to_head    
    if 'chess_com' not in existing_data:
        existing_data['chess_com'] = {}
        
    if 'head_to_head' not in existing_data['chess_com']:
        existing_data['chess_com']['head_to_head'] = {}
        
    updated = False

    # Initialize stats dictionary with default win/loss/draw structure
    stats = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0}))

    for player in players:
        # Check if need to refresh players data
        if (
            player not in existing_data['chess_com']['head_to_head'] 
            or refresh
        ):
            # If player data is missing, or needs refresh, update it
            archives = get_archives(player)
            for archive in archives:
                games = get_games_from_archive(archive)
                for game in games:
                    white = game['white']['username'].lower()
                    black = game['black']['username'].lower()
                    # Decide who is the player and who is the opponent
                    result = game['white']['result'] if white == player else game['black']['result']
                    opponent = black if white == player else white
                    # Only consider games against other tracked players
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
                        updated = True
            # Save the updated stats for the player
            existing_data['chess_com']['head_to_head'][player] = dict(stats[player])

    # Save only if there were updates
    if updated:
        with open(h2h_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4)

    return existing_data['chess_com']['head_to_head']