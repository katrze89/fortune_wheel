from wheel import Wheel


class Game:
    def __init__(self, contestants, word_puzzles):
        self.contestants = contestants
        self.word_puzzles = word_puzzles
        self.wheel = Wheel
        self.letter = ''
        self.vowel = ''
        self.not_guessed_letters = ''

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

    def evaluate_vowel(self, letter):
        if letter in self.vowel:
            print(f'{letter} was already given')
            idxs = []
        elif letter in ['a', 'e', 'i', 'o', 'u', 'y']:
            self.vowel += letter
            idxs = self.word_puzzles.guess_letter(letter)
        else:
            print(f'{letter} is not a vowel')
            idxs = []
        return idxs

    def evaluate_letter(self, letter):
        if letter in self.letter:
            print(f'{letter} was already given')
            idxs = []
        elif not letter.isalpha():
            print(f'{letter} is not a letter')
            idxs = []
        elif letter in ['a', 'e', 'i', 'o', 'u', 'y']:
            print(f'{letter} is a vowel')
            idxs = []
        else:
            self.letter += letter
            idxs = self.word_puzzles.guess_letter(letter)
        return idxs

    def enter_the_letter(self, letter_type, contestant, amount):
        print(f"{contestant.name}, enter a {letter_type}")
        letter = input()
        idxs = self.evaluate_letter(letter) if letter_type == 'letter' else self.evaluate_vowel(letter)
        print(f"You guessed {len(idxs)} {letter_type}")
        contestant.score = amount * len(idxs) if letter_type == 'letter' else amount
        if len(idxs) == 0:
            print(f'{contestant.name} you lost your turn')
            self.contestants.change_player()
            return False
        else:
            self.word_puzzles.update_converted_sentence(idxs)
            self.not_guessed_letters.remove(letter)
        return True

    def end_of_round(self):
        self.show_end('round', 'score')
        self.contestants.reset_scores()
        self.letter = ''
        self.vowel = ''

    def enter_wrong_answer(self):
        print('Wrong answer. You lose your turn.')
        self.contestants.change_player()

    def buy_a_vowel(self, contestant):
        print(f"{contestant.name}, do you want to buy a vowel? It costs PLN 200. [y/n]")
        answer = input()
        if answer.lower() == 'y':
            self.enter_the_letter('vowel', contestant, -200)
        elif answer.lower() != 'n':
            self.enter_wrong_answer()

    def enter_sentence(self, contestant):
        print(f"{contestant.name}, enter the sentence")
        player_sentence = input()
        if player_sentence.lower() == self.word_puzzles.current_sentence.puzzle.lower():
            print(f"{contestant.name}, congratulation you guessed the sentence")
            self.end_of_round()
            return True
        else:
            self.enter_wrong_answer()
            return False

    def play_round(self):
        while True:
            print(self.not_guessed_letters)
            contestant = self.contestants.players[self.contestants.current_player]
            if self.not_guessed_letters.issubset({'a', 'e', 'i', 'o', 'u', 'y'}):
                if contestant.score >= 200:
                    self.buy_a_vowel(contestant)
                print(f'{contestant.name} you have to guess a sentence')
                if self.enter_sentence(contestant):
                    break
            if "_ " not in self.word_puzzles.converted_sentence:
                self.end_of_round()
                break
            amount = self.wheel.spin_wheel()
            if amount == -1:
                self.contestants.change_player()
                print(f'{contestant.name} you lost your turn')
            elif amount == -2:
                contestant.score = amount
                print(f'{contestant.name} you lost your turn and all your money')
                self.contestants.change_player()
            else:
                print(f'One letter is worth PLN {amount}')
                letter_evaluation = self.enter_the_letter('letter', contestant, amount)
                if letter_evaluation:
                    self.show_status('score')
                    print(f"{contestant.name}, do you want to guess a sentence [y/n]")
                    answer = input()
                    if answer.lower() == 'y':
                        if self.enter_sentence(contestant):
                            break
                    elif answer.lower() == 'n':
                        if contestant.score >= 200:
                            self.buy_a_vowel(contestant)
                    else:
                        self.enter_wrong_answer()
            self.show_status('score')

    def play_game(self):
        print(f'How many rounds do you want to play? [max {len(self.word_puzzles.sentences)}]')
        no_rounds = int(input())
        if no_rounds not in range(1, len(self.word_puzzles.sentences)+1):
            raise ValueError('Wrong number of rounds. Game over')
        for no_round in range(no_rounds):
            print("New round")
            self.word_puzzles.__init__(self.word_puzzles.sentences)
            self.word_puzzles.print_converted_sentence()
            self.not_guessed_letters = set(self.word_puzzles.current_sentence.puzzle.lower())
            self.not_guessed_letters.remove(' ')
            self.play_round()
        self.show_end('game', 'total_score')
