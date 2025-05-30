def load_players(path = 'data/players.txt') -> list:
    """Load players from a text file.

    Args:
        path (str, optional): The path to the players file. Defaults to 'data/players.txt'.

    Returns:
        list: A list of player usernames.
    """
    with open(path, 'r', encoding='utf-8') as file:
        # Read lines, strip whitespaces and convert to lowercase
        return [line.strip().lower() for line in file.readlines()]

