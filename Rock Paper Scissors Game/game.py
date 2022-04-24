#!usr/bin/env python3
import random
from itertools import cycle, islice

class Game:

    def __init__(self):
        self.user_selection = None
        self.default_options = ['rock', 'paper', 'scissors']
        self.all_options = ['rock', 'gun', 'lightning', 'devil', 'dragon', 'water', 'air', 'paper', 'sponge', 'wolf', 'tree', 'human', 'snake', 'scissors', 'fire']
        self.other_options =  ['!exit', '!rating']
        self.machine = None
        self.actual_score = 0
        self.file_name = 'rating.txt'
        self.end = False

    def win_or_lose(self):
        if self.user_selection in self.default_options and self.user_selection not in self.other_options:
            user_index = self.all_options.index(self.user_selection)
            circular_list = cycle(self.all_options)
            lose_list = list(islice(circular_list,user_index +1, user_index + 8))
            
            if self.machine in lose_list:
                print('Sorry, but the computer chose', self.machine)
            
            elif self.user_selection == self.machine:
                print('There is a draw', self.machine)
                self.actual_score += 50
            
            else:
                print('Well done. The computer chose', self.machine, 'and failed')
                self.actual_score += 100

    def calculate_score(self, user_name):
        file = open(self.file_name, 'r')
        for line in file:
            scores = line.split()
            if scores[0] == user_name:
                self.actual_score = self.actual_score + int(scores[1])
        file.close()
    
    def game_options(self):
        game_options_input = input().split(',')
        game_options_input = [i for i in game_options_input if i not in ['rock', 'paper', 'scissors','']]
        self.default_options.extend(game_options_input)
        print("Okay, let's start")
       
    def the_game(self):
        user_name = input('Enter your name: ')
        print('Hello,',user_name)    
        self.calculate_score(user_name)  
        self.game_options()
        while not self.end:
            self.user_selection = input()
            self.machine = random.choice(self.default_options)
            self.win_or_lose()
            if self.user_selection == self.other_options[0]:
                print('Bye!')
                self.end = True
            elif self.user_selection == self.other_options[1]:
                print('Your rating:', self.actual_score)
            elif self.user_selection not in self.default_options and  self.user_selection not in self.other_options:
                print('Invalid input')


if __name__ == "__main__":
    Game().the_game()