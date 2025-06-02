def load_players(path: str = 'data/players.txt') -> list:
    """Load a list of player usernames from a text file.

    Each line in the file should contain a single username. Usernames are stripped of
    leading/trailing whitespace and converted to lowercase.

    Args:
        path (str, optional): The path to the players file. Defaults to 'data/players.txt'.

    Returns:
        list: A list of player usernames in lowercase.
            Example: ['player1', 'player2', 'player3']
    """
    with open(path, 'r', encoding='utf-8') as file:
        # Read lines, strip whitespaces and convert to lowercase
        return [line.strip().lower() for line in file.readlines()]

