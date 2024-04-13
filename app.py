import random, os, sys

vowels = ['a', 'e', 'i', 'o', 'u']

def load_words():
    script_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    words_path = os.path.join(script_path, 'words_alpha.txt')
    with open(words_path) as word_file:
        valid_words = list(word_file.read().split())
    return valid_words

def choose_word():
    words = load_words()
    return random.choice(words)

def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters or letter.lower() in vowels:
            display += letter
        else:
            display += "_"
    return display

def hangman():
    while True:
        play_round()

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye.")
            break

def play_round():
    word_to_guess = choose_word()
    guessed_letters = []
    max_attempts = 6
    attempts = 0

    print("Welcome to Hangman!")

    while True:
        current_display = display_word(word_to_guess, guessed_letters)
        if attempts == 0:
            print_hangman(0)
        print("\nCurrent word: " + current_display)
        print(f"You have guessed the following letters: {guessed_letters}")
        print(f"Attempts: {attempts}/{max_attempts}")
        guess = input("Guess a letter: ").lower()

        if guess.isalpha() and len(guess) == 1:
            if guess in guessed_letters:
                print("You already guessed that letter. Try again.")
            elif guess in vowels:
                print("Vowels are automatically revealed. Choose a consonant.")
            elif guess in word_to_guess:
                print("Good guess!")
                guessed_letters.append(guess)
            else:
                print("Wrong guess. Try again!")
                attempts += 1
                print_hangman(attempts)
        else:
            print("Invalid input. Please enter a single letter.")

        if "_" not in display_word(word_to_guess, guessed_letters):
            print("\nCongratulations! You guessed the word: " + word_to_guess)
            break

        if attempts == max_attempts:
            print("\nSorry, you ran out of attempts. The word was: " + word_to_guess)
            break

def print_hangman(attempts):
    hangman_graphics = [
        """
         -----
         |   |
             |
             |
             |
             |
        """,
        """
         -----
         |   |
         O   |
             |
             |
             |
        """,
        """
         -----
         |   |
         O   |
         |   |
             |
             |
        """,
        """
         -----
         |   |
         O   |
        /|   |
             |
             |
        """,
        """
         -----
         |   |
         O   |
        /|\\  |
             |
             |
        """,
        """
         -----
         |   |
         O   |
        /|\\  |
        /    |
             |
        """,
        """
         -----
         |   |
         O   |
        /|\\  |
        / \\  |
             |
        """
    ]
    print(hangman_graphics[attempts])

if __name__ == "__main__":
    hangman()
