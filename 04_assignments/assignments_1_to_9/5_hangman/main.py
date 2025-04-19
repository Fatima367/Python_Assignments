import random
from words import words
import string

def get_valid_words(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word.upper()

def hangman():
    word = get_valid_words(words)
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()

    lives = 7

    # for getting user input
    while len(word_letters) > 0 and lives > 0:
        # letters used
        print(f"Lives Left: {lives}")
        print(f"Used letters: {" ".join(sorted(used_letters))}")

        # what current word is for example ( W _ O R D)
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print(f"Current Word: {" ".join(word_list)}")

        user_letter = input("Guess a letter: ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print('')

            else:
                lives -= 1
                print(f"Your letter {user_letter} is not in the word.")
        else:
            print("Not a valid letter.")

    if lives == 0:
        print(f"You lost, sorry.\nThe word was: {word}")
    else:
        print(f"Yay!! you guessed the word {word} correctly!!")

if __name__ == '__main__':
    hangman()