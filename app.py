from random import randint


class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    @property
    def score(self):
        return f"{self._score}PLN"

    @score.setter
    def score(self, new_value):
        self._score = self.score + new_value if new_value != 0 else 0


class Players:
    def __init__(self, players):
        self.players = players
        self.current_player = 0

    def change_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)


class Wheel:

    @staticmethod
    def spin_wheel():
        wheel = [100, 200, 300, 400, 500, 0, -1]
        return wheel[randint(0, len(wheel) - 1)]


class Board:
    pass


class Game:
    pass
