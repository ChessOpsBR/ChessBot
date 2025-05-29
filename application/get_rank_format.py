class ChessStats:
    def __init__(self, player_name, data: dict):
        self.player_name = player_name
        self.data = data

    def get_rapid_stats(self): return self.data.get('chess_rapid', {})
    def get_blitz_stats(self): return self.data.get('chess_blitz', {})
    def get_bullet_stats(self): return self.data.get('chess_bullet', {})

    def get_actual_rank(self):
        def safe_get_rating(stats, key): return stats.get(key, {}).get('rating', 0)
        def safe_get_record(stats, key): return stats.get('record', {}).get(key, 0)

        classic = self.get_rapid_stats()
        blitz = self.get_blitz_stats()
        bullet = self.get_bullet_stats()

        return {
            self.player_name: {
                'classic': {
                    'classic': safe_get_rating(classic, 'last'),
                    'best_classic': safe_get_rating(classic, 'best'),
                    'difference': safe_get_rating(classic, 'last') - safe_get_rating(classic, 'best'),
                    'record': {
                        'wins': safe_get_record(classic, 'win'),
                        'losses': safe_get_record(classic, 'loss'),
                        'draws': safe_get_record(classic, 'draw'),
                        'win_loss_diff': safe_get_record(classic, 'win') - safe_get_record(classic, 'loss'),
                    }
                },
                'blitz': {
                    'blitz': safe_get_rating(blitz, 'last'),
                    'best_blitz': safe_get_rating(blitz, 'best'),
                    'difference': safe_get_rating(blitz, 'last') - safe_get_rating(blitz, 'best'),
                    'record': {
                        'wins': safe_get_record(blitz, 'win'),
                        'losses': safe_get_record(blitz, 'loss'),
                        'draws': safe_get_record(blitz, 'draw'),
                        'win_loss_diff': safe_get_record(blitz, 'win') - safe_get_record(blitz, 'loss'),
                    }
                },
                'bullet': {
                    'bullet': safe_get_rating(bullet, 'last'),
                    'best_bullet': safe_get_rating(bullet, 'best'),
                    'difference': safe_get_rating(bullet, 'last') - safe_get_rating(bullet, 'best'),
                    'record': {
                        'wins': safe_get_record(bullet, 'win'),
                        'losses': safe_get_record(bullet, 'loss'),
                        'draws': safe_get_record(bullet, 'draw'),
                        'win_loss_diff': safe_get_record(bullet, 'win') - safe_get_record(bullet, 'loss'),
                    }
                },
            }
        }