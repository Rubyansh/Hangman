import tkinter as tk
from PIL import Image, ImageTk
import random, os, sys

vowels = ['a', 'e', 'i', 'o', 'u']

class Hangman:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman - CS Term 2 Project")
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        self.master.iconbitmap(icon_path)
        self.create_widgets()
        self.restart_game()

    def load_words(self):
        script_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        words_path = os.path.join(script_path, 'words_alpha.txt')

        with open(words_path) as word_file:
            valid_words = list(word_file.read().split())
        return valid_words

    def choose_word(self):
        words = self.load_words()
        return random.choice(words)

    def display_word(self):
        display = ""
        for letter in self.word_to_guess:
            if letter in self.guessed_letters or letter.lower() in vowels:
                display += letter
            else:
                display += "_"
        return display

    def create_widgets(self):
        self.hangman_image_label = tk.Label(self.master)
        self.hangman_image_label.pack(pady=10, expand=True)

        self.current_word_label = tk.Label(self.master, text="", font=("Helvetica", 16))
        self.current_word_label.pack(pady=10)

        self.guess_label = tk.Label(self.master, text="Enter a letter:")
        self.guess_label.pack()

        self.guess_entry = tk.Entry(self.master, font=("Helvetica", 14))
        self.guess_entry.pack()

        self.guess_button = tk.Button(self.master, text="Guess", command=self.process_guess)
        self.guess_button.pack(pady=10)

        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart_game)
        self.restart_button.pack(pady=10)

        self.info_label = tk.Label(self.master, text="")
        self.info_label.pack()

        self.guessed_letters_label = tk.Label(self.master, text="Guessed Letters:")
        self.guessed_letters_label.pack()

        self.remaining_attempts_label = tk.Label(self.master, text="")
        self.remaining_attempts_label.pack()
        
        self.master.bind("<Configure>", self.handle_resize)

    def update_hangman(self):
        script_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        image_path = os.path.join(script_path, f"img/hangman_{self.attempts}.png")
        hangman_image = Image.open(image_path)
        self.original_hangman_image = ImageTk.PhotoImage(hangman_image)

        self.hangman_image_label.config(image=self.original_hangman_image)

    def handle_resize(self, event):
        self.update_hangman()

    def process_guess(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if guess.isalpha() and len(guess) == 1:
            if guess in self.guessed_letters or guess in self.incorrect_letters:
                self.info_label.config(text="You already guessed that letter. Try again.")
            elif guess in vowels:
                self.info_label.config(text="Vowels are automatically revealed. Choose a consonant.")
            elif guess in self.word_to_guess:
                self.info_label.config(text="Good guess!")
                self.guessed_letters.append(guess)
            else:
                self.info_label.config(text="Wrong guess. Try again!")
                self.incorrect_letters.append(guess)
                self.attempts += 1
                self.remaining_attempts -= 1

            self.current_word_label.config(text=self.display_word())
            self.update_hangman()
            self.update_guessed_letters_label()
            self.update_remaining_attempts_label()

            if "_" not in self.display_word():
                self.info_label.config(text=f"Congratulations! You guessed the word: {self.word_to_guess}")
                self.disable_input()
            elif self.remaining_attempts == 0:
                self.info_label.config(text=f"Sorry, you ran out of attempts. The word was: {self.word_to_guess}")
                self.disable_input()
                
        else:
            self.info_label.config(text="Invalid input. Please enter a single letter.")

    def update_guessed_letters_label(self):
        guessed_letters = set(self.guessed_letters + [letter for letter in self.incorrect_letters if letter not in vowels])
        self.guessed_letters_label.config(text="Guessed Letters: " + ", ".join(sorted(guessed_letters)))

    def update_remaining_attempts_label(self):
        self.remaining_attempts_label.config(text=f"Remaining Attempts: {self.remaining_attempts}")

    def disable_input(self):
        self.guess_entry.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)

    def enable_input(self):
        self.guess_entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)

    def restart_game(self):
        self.word_to_guess = self.choose_word()
        self.guessed_letters = []
        self.incorrect_letters = []
        self.attempts = 0
        self.max_attempts = 6
        self.remaining_attempts = self.max_attempts
        self.info_label.config(text="")
        self.current_word_label.config(text=self.display_word())
        self.remaining_attempts_label.config(text=f"Remaining Attempts: {self.remaining_attempts}")
        self.enable_input()
        self.update_hangman()

def main():
    root = tk.Tk()
    hangman_game = Hangman(root)
    root.mainloop()

if __name__ == "__main__":
    main()
