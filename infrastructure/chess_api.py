import requests
from infrastructure.headers import HEADERS

def get_player_info(username: str) -> dict:
    url = f"https://api.chess.com/pub/player/{username}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f'HTTP Error: {errh}')
        return {}

def get_player_stats(username: str) -> dict:
    url = f"https://api.chess.com/pub/player/{username}/stats"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f'HTTP Error: {errh}')
        return {}

def get_archives(username: str) -> list:
    url = f'https://api.chess.com/pub/player/{username}/games/archives'
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get('archives', [])
    except requests.exceptions.HTTPError as errh:
        print(f'HTTP Error: {errh}')
        return []

def get_games_from_archive(archive_url: str) -> list:
    try:
        response = requests.get(archive_url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get('games', [])
    except requests.exceptions.HTTPError as errh:
        print(f'HTTP Error: {errh}')
        return []