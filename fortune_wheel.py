from player import Player
from players import Players
from board import Board
from game import Game
from word_puzzle import WordPuzzle


def play():
    jon = Player('Jon', -2, 0)
    jessica = Player('Jessica', -2, 0)
    bryan = Player('Bryan', -2, 0)
    contestants = Players([jon, jessica, bryan])
    sentence_1 = WordPuzzle('Ala ma kota')
    sentence_2 = WordPuzzle('Baba z wozu koniom lzej')
    sentence_3 = WordPuzzle('Jak Kuba bogu tak bog Kubie')
    word_puzzles = Board([sentence_1, sentence_2, sentence_3])
    game = Game(contestants, word_puzzles)
    game.play_game()


if __name__ == '__main__':
    play()
