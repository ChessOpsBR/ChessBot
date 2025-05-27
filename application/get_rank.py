from infrastructure.player_stats_api import Api

class ChessStats:
    def __init__(self, player_name, data: dict):
        """
        player_name: nome do jogador, usado para o json
        data: dicionario que contem os dados do jogador
        """
        self.player_name = player_name
        self.data = data

    def get_rapid_stats(self) -> dict:
        chess_rapid = self.data.get('chess_rapid', {})
        return chess_rapid

    def get_blitz_stats(self) -> dict:
        chess_blitz = self.data.get('chess_blitz', {})
        return chess_blitz

    def get_bullet_stats(self) -> dict:
        bullet = self.data.get('chess_bullet', {})
        return bullet
    
    def get_actual_rank(self) -> dict:

        classic = self.get_rapid_stats()
        blitz = self.get_blitz_stats()
        bullet = self.get_bullet_stats()
        
        def safe_get_rating(stats, key):
            return stats.get(key, {}).get('rating', 0)

        def safe_get_record(stats, key):
            return stats.get('record', {}).get(key, 0)

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