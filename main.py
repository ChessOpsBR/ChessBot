import json
from helpers.data_loader import load_players
from application.get_rank import get_all_ratings_summary
from application.get_head_to_head import get_all_head_to_head

# Load the list of player usernames from file
def main():
    player_usernames = load_players()

    # Build the output dictionary with player ratings and head-to-head stats
    output = {
        "chess_com": {
            "players_ratings_summary": get_all_ratings_summary(player_usernames),
            "head_to_head": get_all_head_to_head(player_usernames)
        }
    }

    # Save the output to a JSON file
    with open('data/rank.json', 'w', encoding='utf-8') as file:
        json.dump(output, file, indent=4)

if __name__ == "__main__":
    main()
