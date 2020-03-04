from wheel import Wheel


class Game:
    def __init__(self, contestants, word_puzzles):
        self.contestants = contestants
        self.word_puzzles = word_puzzles
        self.wheel = Wheel
        self.letter = ''

    def show_status(self, score):
        frame = f'+{"-" * 33}+'
        line = f'|{" " * 33}|'
        users = f'|{" | ".join([n.name.center(9) for n in self.contestants.players])}|'
        if score == 'score':
            scores = f'|{" | ".join([str(n.score).center(9) for n in self.contestants.players])}|'
            current = f'|{" | ".join(["X".center(9) if n == self.contestants.current_player else " " * 9 for n in range(len(self.contestants.players))])}|'
            self.word_puzzles.print_converted_sentence()
            banner = [frame, line, users, scores, current, line, frame]
        else:
            scores = f'|{" | ".join([str(n.total_score).center(9) for n in self.contestants.players])}|'
            banner = [frame, line, users, scores, line, frame, '']
        print("\n".join(banner))

    def show_end(self, stage, score_type):
        print(f'End of {stage}')
        if score_type == 'score':
            players_score = [(idx, n.score) for idx, n in enumerate(self.contestants.players)]
        else:
            players_score = [(idx, n.total_score) for idx, n in enumerate(self.contestants.players)]
        ms = max(players_score, key=lambda item: item[1])
        print(f"Congratulation {self.contestants.players[ms[0]].name} You won {stage} and scored {ms[1]} points.")
        if stage == 'round':
            self.contestants.players[ms[0]].update_total_score(ms[1])
            self.show_status('total_score')

    def evaluate_letter(self, letter):
        if letter in self.letter:
            print(f'{letter} was already given')
            idxs = []
        elif not letter.isalpha():
            print(f'{letter} is not a letter')
            idxs = []
        else:
            self.letter += letter
            idxs = self.word_puzzles.guess_letter(letter)
        return idxs

    def play_round(self):
        while True:
            if "_ " not in self.word_puzzles.converted_sentence:
                self.show_end('round', 'score')
                self.contestants.reset_scores()
                self.letter = ''
                break
            amount = self.wheel.spin_wheel()
            contestant = self.contestants.players[self.contestants.current_player]
            if amount == -1:
                self.contestants.change_player()
                print(f'{contestant.name} you lost your turn')
            elif amount == 0:
                contestant.score = amount
                self.contestants.change_player()
                print(f'{contestant.name} you lost your turn and all your money')
            else:
                print(f'One letter is worth PLN {amount}')
                print(f"{contestant.name}, enter a letter")
                letter = input()
                idxs = self.evaluate_letter(letter)
                print(f"You guessed {len(idxs)} letters")
                if len(idxs) == 0:
                    self.contestants.change_player()
                else:
                    self.word_puzzles.update_converted_sentence(idxs)
                    contestant.score = amount * len(idxs)
            self.show_status('score')

    def play_game(self):
        print(f'How many rounds do you want to play? [max {len(self.word_puzzles.sentences)}]')
        no_rounds = int(input())
        for no_round in range(no_rounds):
            self.word_puzzles.__init__(self.word_puzzles.sentences)
            self.word_puzzles.print_converted_sentence()
            self.play_round()
        self.show_end('game', 'total_score')
