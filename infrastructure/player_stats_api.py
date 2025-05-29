from infrastructure.chess_api import get_player_stats, get_player_info

class Api:
    def __init__(self, player_name: str):
        self.player_name = player_name

    def get_player_info(self) -> dict:
        return get_player_info(self.player_name)

    def get_status(self) -> dict:
        return get_player_stats(self.player_name)