# Class to represent chess statistics for a player
class ChessStats:
    """
    Class to represent chess statistics for a player.
    """
    def __init__(self, player_name, data: dict):
        """Initialize the ChessStats object.

        Args:
            player_name (str): The name of the player.
            data (dict): The player's statistics data.
        """
        self.player_name = player_name
        self.data = data

    def get_rapid(self):
        """Get the player's rapid chess statistics.

        Returns:
            dict: Rapid chess statistics.
        """
        return self.data.get('chess_rapid', {})

    def get_blitz(self):
        """Get the player's blitz chess statistics.

        Returns:
            dict: Blitz chess statistics.
        """
        return self.data.get('chess_blitz', {})

    def get_bullet(self):
        """Get the player's bullet chess statistics.

        Returns:
            dict: Bullet chess statistics.
        """
        return self.data.get('chess_bullet', {})

    def get_ratings_summary(self):
        """Get a summary of the player's ratings and records in different formats.

        Returns:
            dict: Player's ratings and records by format (classic, blitz, bullet).
        """
        def get_rating(stats: dict, key: str) -> int:
            """Get the rating for a specific chess format.

            Args:
                stats (dict): Player's statistics.
                key (str): Format key ('last', 'best').

            Returns:
                int: Rating for the specified format.
            """
            return stats.get(key, {}).get('rating', 0)

        def get_record(stats, key):
            """Get the record for a specific chess format.

            Args:
                stats (dict): Player's statistics.
                key (str): Record key ('win', 'loss', 'draw').

            Returns:
                int: Value of the specified record.
            """
            return stats.get('record', {}).get(key, 0)

        # Get statistics for each format
        classic = self.get_rapid()
        blitz = self.get_blitz()
        bullet = self.get_bullet()

        # Return the dictionary with ratings and records
        return {
            self.player_name: {
                'classic': {
                    'current': get_rating(classic, 'last'),
                    'best': get_rating(classic, 'best'),
                    'difference': get_rating(classic, 'last') - get_rating(classic, 'best'),
                    'record': {
                        'wins': get_record(classic, 'win'),
                        'losses': get_record(classic, 'loss'),
                        'draws': get_record(classic, 'draw'),
                        'win_loss_diff': get_record(classic, 'win') - get_record(classic, 'loss'),
                    }
                },
                'blitz': {
                    'current': get_rating(blitz, 'last'),
                    'best': get_rating(blitz, 'best'),
                    'difference': get_rating(blitz, 'last') - get_rating(blitz, 'best'),
                    'record': {
                        'wins': get_record(blitz, 'win'),
                        'losses': get_record(blitz, 'loss'),
                        'draws': get_record(blitz, 'draw'),
                        'win_loss_diff': get_record(blitz, 'win') - get_record(blitz, 'loss'),
                    }
                },
                'bullet': {
                    'current': get_rating(bullet, 'last'),
                    'best': get_rating(bullet, 'best'),
                    'difference': get_rating(bullet, 'last') - get_rating(bullet, 'best'),
                    'record': {
                        'wins': get_record(bullet, 'win'),
                        'losses': get_record(bullet, 'loss'),
                        'draws': get_record(bullet, 'draw'),
                        'win_loss_diff': get_record(bullet, 'win') - get_record(bullet, 'loss'),
                    }
                },
            }
        }