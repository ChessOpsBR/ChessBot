import requests
from infrastructure.headers import HEADERS

def get_player_info(username: str) -> dict:
    """
    Fetch general information about a player from the Chess.com API.

    Args:
        username (str): The Chess.com username.

    Returns:
        dict: Player information as returned by the API, or an empty dict on error.
    """
    url = f"https://api.chess.com/pub/player/{username}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f'HTTP Error: {errh}')
        return {}

def get_player_stats(username: str) -> dict:
    """
    Fetch chess statistics for a player from the Chess.com API.

    Args:
        username (str): The Chess.com username.

    Returns:
        dict: Player statistics as returned by the API, or an empty dict on error.
    """
    url = f"https://api.chess.com/pub/player/{username}/stats"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f'HTTP Error: {errh}')
        return {}

def get_archives(username: str) -> list:
    """
    Fetch the list of archive URLs for a player's games from the Chess.com API.

    Args:
        username (str): The Chess.com username.

    Returns:
        list: List of archive URLs, or an empty list on error.
    """
    url = f'https://api.chess.com/pub/player/{username}/games/archives'
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get('archives', [])
    except requests.exceptions.HTTPError as errh:
        print(f'HTTP Error: {errh}')
        return []

def get_games_from_archive(archive_url: str) -> list:
    """
    Fetch all games from a specific archive URL from the Chess.com API.

    Args:
        archive_url (str): The URL of the archive.

    Returns:
        list: List of games, or an empty list on error.
    """
    try:
        response = requests.get(archive_url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get('games', [])
    except requests.exceptions.HTTPError as errh:
        print(f'HTTP Error: {errh}')
        return []