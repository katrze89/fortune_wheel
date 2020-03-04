from random import randint


class Board:
    def __init__(self, sentences):
        self.sentences = sentences
        self.current_sentence = self.shuffle_sentence()
        self.converted_sentence = self.convert_sentence()

    def print_converted_sentence(self):
        print("".join(self.converted_sentence))

    def update_converted_sentence(self, idxs):
        for idx in idxs:
            self.converted_sentence[idx] = self.current_sentence.puzzle[idx]+' '

    def shuffle_sentence(self):
        while True:
            rand_num = randint(0, len(self.sentences) - 1)
            if self.sentences[rand_num].status:
                self.sentences[rand_num].status = False
                return self.sentences[rand_num]

    def guess_letter(self, letter):
        idx_letter = [idx for idx, c in enumerate(self.current_sentence.puzzle) if c.lower() == letter]
        return idx_letter

    def convert_sentence(self):
        sentence = self.current_sentence.puzzle
        return ["_ " if char.isalpha() else u"\u25A0 " if char == " " else char + ' ' for char in sentence]
