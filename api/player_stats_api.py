from infrastructure.chess_api import get_player_stats, get_player_info

class Api:
    """
    Wrapper class for accessing player information and statistics from Chess.com API.
    """
    def __init__(self, player_name: str):
        """
        Initialize the Api object with a player's username.

        Args:
            player_name (str): The Chess.com username.
        """
        self.player_name = player_name

    def get_player_info(self) -> dict:
        """
        Retrieve general information about the player.

        Returns:
            dict: Player information as returned by the API.
        """
        return get_player_info(self.player_name)

    def get_status(self) -> dict:
        """
        Retrieve chess statistics for the player.

        Returns:
            dict: Player statistics as returned by the API.
        """
        return get_player_stats(self.player_name)