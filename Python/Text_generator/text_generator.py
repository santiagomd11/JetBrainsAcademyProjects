from nltk.tokenize import WhitespaceTokenizer
import operator
import random
import re


class TextGenerator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.__token_array = []
        self.__wts = WhitespaceTokenizer()
        self.__bigram = None
        self.__markov_dict = {}
        self.__end = False

    def tokenize(self):
        with open(self.file_name, "r", encoding="utf-8") as f:
            for line in f.readlines():
                self.__token_array.extend(self.__wts.tokenize(line))

    def get_markov_dict(self):
        for element in self.__bigram:
            self.__markov_dict.setdefault(element[0], {}).setdefault(element[1], 0)
            self.__markov_dict[element[0]][element[1]] += 1

    def get_most_probable_word(self, input_word):
        most_probable = max(self.__markov_dict[input_word].items(), key=operator.itemgetter(1))[0]
        return most_probable

    def play(self):
        self.tokenize()
        self.__bigram = [[self.__token_array[i], self.__token_array[i + 1]] for i in range(0, len(self.__token_array) - 1)]
        self.get_markov_dict()
        for _ in range(0, 10):
            word = random.choice(list(self.__markov_dict.keys()))
            sentence = ""
            for i in range(0, 10):
                if len(sentence.split()) >= 5 and sentence.split()[-1][-1] in '.?!':
                    break
                if not sentence:
                    while not word[0].isupper() or not word[-1].isalpha():
                        word = random.choice(list(self.__markov_dict.keys()))
                if i == 9:
                    while not re.match(r'.+[.?!]$', word):
                        word = random.choice(list(self.__markov_dict.keys()))
                    sentence += f'{word} '
                    break
                sentence += f'{word} '
                word = self.get_most_probable_word(word)
            print(sentence)


if __name__ == "__main__":
    file_name_input = input()
    text_generator = TextGenerator(file_name_input)
    text_generator.play()
