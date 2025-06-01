import json

def load_rank_data(path='data/rank.json') -> dict:
    with open(path, 'r') as file:
        return json.load(file)
    
data = load_rank_data()

print(data['chess_com']['players_ratings_summary'][0])