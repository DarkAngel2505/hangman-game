import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    """
    A personalized Hangman game with a graphical interface, custom word list, and score tracking.
    Created by [Your Name] for portfolio demonstration.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman by [Your Name]")
        self.root.geometry("600x600")
        self.root.configure(bg="#e6f3fa")  # Light blue background for a unique look

        # Custom word list (e.g., themed around hobbies or interests)
        self.words = ['GUITAR', 'PAINTING', 'HIKING', 'CODING', 'TRAVEL', 'READING']
        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.remaining_tries = 6
        self.score = 0  # Track player's score

        # GUI Elements
        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="white", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.draw_hangman(0)  # Initial hangman drawing

        self.word_display = tk.Label(self.root, text=self.get_display_word(), font=("Helvetica", 24, "bold"), bg="#e6f3fa")
        self.word_display.pack(pady=20)

        self.status_label = tk.Label(self.root, text=f"Tries left: {self.remaining_tries} | Score: {self.score}",
                                    font=("Helvetica", 14), bg="#e6f3fa")
        self.status_label.pack()

        # Letter buttons frame
        self.button_frame = tk.Frame(self.root, bg="#e6f3fa")
        self.button_frame.pack(pady=20)

        # Create letter buttons with custom styling
        self.letter_buttons = {}
        for i, letter in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            btn = tk.Button(self.button_frame, text=letter, command=lambda l=letter: self.guess_letter(l),
                            width=3, font=("Helvetica", 12), bg="#4a90e2", fg="white", relief="flat")
            btn.grid(row=i // 7, column=i % 7, padx=2, pady=2)
            self.letter_buttons[letter] = btn

        # Score display
        self.score_label = tk.Label(self.root, text=f"High Score: {self.score}", font=("Helvetica", 12), bg="#e6f3fa")
        self.score_label.pack()

        # Bind keyboard input
        self.root.bind("<Key>", self.handle_keypress)

        # New Game button
        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game,
                                        font=("Helvetica", 12), bg="#ff6b6b", fg="white")
        self.new_game_button.pack(pady=10)

    def draw_hangman(self, stage):
        """Draws the hangman figure progressively on the canvas."""
        self.canvas.delete("all")
        # Gallows
        self.canvas.create_line(50, 180, 150, 180, width=2)  # Base
        self.canvas.create_line(100, 180, 100, 20, width=2)  # Pole
        self.canvas.create_line(100, 20, 140, 20, width=2)   # Top
        self.canvas.create_line(140, 20, 140, 40, width=2)   # Rope

        # Hangman parts based on stage
        if stage >= 1:  # Head
            self.canvas.create_oval(130, 40, 150, 60, width=2)
        if stage >= 2:  # Body
            self.canvas.create_line(140, 60, 140, 100, width=2)
        if stage >= 3:  # Left arm
            self.canvas.create_line(140, 70, 120, 90, width=2)
        if stage >= 4:  # Right arm
            self.canvas.create_line(140, 70, 160, 90, width=2)
        if stage >= 5:  # Left leg
            self.canvas.create_line(140, 100, 120, 130, width=2)
        if stage >= 6:  # Right leg
            self.canvas.create_line(140, 100, 160, 130, width=2)

    def get_display_word(self):
        """Returns the word with underscores for unguessed letters."""
        return ' '.join(letter if letter in self.guessed_letters else '_' for letter in self.word)

    def guess_letter(self, letter):
        """Processes a letter guess."""
        letter = letter.upper()
        if letter in self.letter_buttons and self.remaining_tries > 0:
            self.letter_buttons[letter].config(state="disabled", bg="#cccccc")
            self.guessed_letters.add(letter)

            if letter not in self.word:
                self.remaining_tries -= 1
                self.draw_hangman(6 - self.remaining_tries)
                self.status_label.config(text=f"Tries left: {self.remaining_tries} | Score: {self.score}")
            else:
                self.score += 10  # Award points for correct guess
                self.status_label.config(text=f"Tries left: {self.remaining_tries} | Score: {self.score}")

            self.word_display.config(text=self.get_display_word())
            self.check_game_status()

    def handle_keypress(self, event):
        """Handles keyboard input for letter guesses."""
        letter = event.char.upper()
        if letter.isalpha() and letter in self.letter_buttons and self.letter_buttons[letter]["state"] != "disabled":
            self.guess_letter(letter)

    def check_game_status(self):
        """Checks if the game is won or lost."""
        if all(letter in self.guessed_letters for letter in self.word):
            self.score += 50  # Bonus for winning
            self.score_label.config(text=f"High Score: {self.score}")
            messagebox.showinfo("Hangman", f"Congratulations! You won!\nScore: {self.score}")
            self.disable_all_buttons()
        elif self.remaining_tries <= 0:
            messagebox.showinfo("Hangman", f"Game Over! The word was {self.word}\nScore: {self.score}")
            self.score_label.config(text=f"High Score: {self.score}")
            self.disable_all_buttons()

    def disable_all_buttons(self):
        """Disables all letter buttons."""
        for button in self.letter_buttons.values():
            button.config(state="disabled", bg="#cccccc")

    def new_game(self):
        """Resets the game for a new round."""
        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.remaining_tries = 6
        self.draw_hangman(0)
        self.word_display.config(text=self.get_display_word())
        self.status_label.config(text=f"Tries left: {self.remaining_tries} | Score: {self.score}")
        for button in self.letter_buttons.values():
            button.config(state="normal", bg="#4a90e2")

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()