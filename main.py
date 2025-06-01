import json
from helpers.data_loader import load_players
from application.get_rank import get_all_ratings_summary

def main():
    """
    Loads player usernames and updates chess ratings summary incrementally.
    """
    player_usernames = load_players()

    # Get the updated ratings summary as a dictionary
    players_ratings_summary = get_all_ratings_summary(player_usernames)

    # Save the output to a JSON file (optional, since get_all_ratings_summary may already handle this)
    with open('data/rank.json', 'w', encoding='utf-8') as file:
        json.dump({"chess_com": {"players_ratings_summary": players_ratings_summary}}, file, indent=4)

if __name__ == "__main__":
    main()
