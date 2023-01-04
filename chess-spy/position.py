class Position:

    positions = {}

    @classmethod
    def from_fen(cls, fen):
        # stripped_fen does not include the half move clock or whole move clock
        # ex:
        #     "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
        #       becomes
        #     "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq -"
        stripped_fen = " ".join(fen.split()[:-2])
        position = cls.positions.get(stripped_fen)
        if not position:
            position = cls(stripped_fen)
            cls.positions[stripped_fen] = position
        return position

    def __init__(self, stripped_fen):
        self.stripped_fen = stripped_fen
        self.games = []

    def add_game(self, game):
        if not self.game_is_recorded(game):
            self.games.append(game)

    def game_is_recorded(self, game):
        matches = sum(1 for saved_game in self.games if saved_game == game)
        return bool(matches)
