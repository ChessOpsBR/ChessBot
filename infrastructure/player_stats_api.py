import requests
from infrastructure.headers import HEADERS

class Api():
    def __init__(self, player_name: str):
        self.headers = HEADERS
        self.player_name = player_name


    def get_player_info(self) -> dict:
            """
            Get basic player information from Chess.com API, like
            username, player ID, and profile URL.

            Returns:
                dict: The player's information or an error message.
            """
            url = f"https://api.chess.com/pub/player/{self.player_name}"

            try:
                response = requests.get(url= url, headers= self.headers)
                response.raise_for_status()

                if response.status_code == 200:
                    data = response.json()
                    return data
                
            except requests.exceptions.HTTPError as errh:
                print(f'Http Error: {errh}')

    def get_status(self) -> dict:
            """Get the status of a player from Chess.com API.

            Args:
                player_name (str): The username of the player.

            Returns:
                dict: The player's status or an error message.
            """

            url = f"https://api.chess.com/pub/player/{self.player_name}/stats"
        
            try:
                response = requests.get(url=url, headers=self.headers)
                response.raise_for_status()

                if response.status_code == 200:
                    data = response.json()
                    return data
                
            except requests.exceptions.HTTPError as errh:
                print(f'Http Error: {errh}')
            
