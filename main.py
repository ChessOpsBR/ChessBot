from helpers.data_loader import load_players
from application.get_rank import get_rank_json
from application.get_head_to_head import get_head_to_head_json

def main():
    """
    Loads player usernames from a text file and updates chess ratings summary and head-to-head statistics incrementally.
    Also prints the execution time in seconds.

    Steps:
        1. Loads the list of player usernames from 'data/players.txt'.
        2. Updates the ratings summary for each player, only fetching new or outdated data.
        3. Updates the head-to-head statistics for each player, only fetching new or outdated data.
        4. Print the total execution time.
    """
    
    player_usernames = load_players()

    # Update ratings summary and head-to-head statistics
    get_rank_json(player_usernames)
    get_head_to_head_json(player_usernames)
    print('Data updated')

if __name__ == "__main__":
    main()
