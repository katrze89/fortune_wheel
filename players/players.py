class Players:
    def __init__(self, players):
        self.players = players
        self.current_player = 0

    def change_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def reset_scores(self):
        for player in self.players:
            player.score = 0
