from collections import Counter
from random import choice

import sys

# globals
DICTIONARY = set()

# no-op if invalid int supplied
def set_color(i):
    if 31 <= i <= 36:
        print(f'\033[{i}m', end='')

# reset terminal output's color
def reset_color():
    print('\033[39m', end='')

# print `text` with no color formatting
def print_regular(text):
    print(text, end='')

# print `text` in yellow
def print_yellow(text):
    set_color(33)
    print(text, end='')
    reset_color()

# print `text` in green
def print_green(text):
    set_color(32)
    print(text, end='')
    reset_color()

# load words from dict
# dict == enable1.txt with 5-letter words selected
def load_words():
    global DICTIONARY
    with open('dict.txt', 'r') as f:
        DICTIONARY = set(line.strip().upper() for line in f.readlines())

# return a comparison array of `guess` against `target`
# 0 = not present, 1 = present but not in that index, 2 = present
# and in that index
def compare(guess, target):
    result = [(c, 1) for c in guess]
    eliminated_letters = set()
    target_counter = Counter(target)
    for i, c in enumerate(guess):
        if c not in target:
            result[i] = (c, 0)
            eliminated_letters.add(c)
        elif target[i] == c:
            result[i] = (c, 2)
            target_counter[c] -= 1
    for i, c in enumerate(guess):
        if c in target and target[i] != c and target_counter[c] == 0:
            result[i] = (c, 0)
            eliminated_letters.add(c)
    return result, eliminated_letters

# run a comparison then render it nicely
# return True iff the guess was correct
def compare_and_print(guess, target):
    comparison, eliminated_letters = compare(guess, target)
    for c, status in comparison:
        if status == 0:
            print_regular(c)
            print('', end=' ')
        elif status == 1:
            print_yellow(c)
            print('', end=' ')
        elif status == 2:
            print_green(c)
            print('', end=' ')
    print()
    return all(status == 2 for c, status in comparison), eliminated_letters

# print all letters that haven't been eliminated yet
def print_available_letters(eliminated_letters):
    print('Available letters: ', end='')
    for i in range(ord('A'), ord('Z')+1):
        letter = chr(i)
        if letter not in eliminated_letters:
            print_regular(chr(i))
            print('', end=' ')
    print()

# print victory message announcing the number of guesses
def print_victory_message(guess_number):
    guesses = 'guesses' if guess_number > 1 else 'guess'
    print(f'Good job! You took {guess_number} {guesses}.')

# print defeat message announcing the target word
def print_defeat_message(guess_number):
    print(f'Tough luck. The word was {target}')

# check if a guess is in the dictionary
def check_guess(guess):
    return guess in DICTIONARY

if __name__ == '__main__':
    target = choice(DICTIONARY)
    eliminated_letters = set()
    for guess_number in range(1, 7):
        valid_guess = True
        while valid_guess:
            print_available_letters(eliminated_letters)
            print(f'Guess #{guess_number}: ', end='')
            guess = input().upper()
            valid_guess = check_guess(guess)
        correct, eliminated_letters = compare_and_print(guess, target)
        if correct:
            print_victory_message(guess_number)
            sys.exit(0)
    print_defeat_message(target)
