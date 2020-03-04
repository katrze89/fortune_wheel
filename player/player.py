class Player:
    def __init__(self, name, score, total_score=0):
        self.name = name
        self.score = score
        self.total_score = total_score

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, new_value):
        self._score = self.score + new_value if new_value != 0 else 0

    def update_total_score(self, new_value):
        self.total_score += new_value
