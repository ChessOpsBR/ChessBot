def load_players(path='data/players.txt'):
    with open(path, 'r', encoding='utf-8') as file:
        return [line.strip().lower() for line in file.readlines()]