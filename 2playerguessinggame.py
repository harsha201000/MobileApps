from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from random import randint
from kivy.core.window import Window

# Global variables
player_turn = 1
secret_number = randint(1, 100)
player_scores = {1: 0, 2: 0}

class GuessingGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Instructions Label
        self.instructions_label = Label(
            text="Player 1, guess the number (1-100):", font_size="20sp"
        )
        self.add_widget(self.instructions_label)

        # Input for guessing
        self.guess_input = TextInput(multiline=False, font_size="20sp", size_hint=(1, 0.2))
        self.add_widget(self.guess_input)

        # Submit Button
        self.submit_button = Button(text="Submit Guess", size_hint=(1, 0.2))
        self.submit_button.bind(on_press=self.check_guess)
        self.add_widget(self.submit_button)

        # Feedback Label
        self.feedback_label = Label(text="", font_size="18sp", color=(1, 0, 0, 1))
        self.add_widget(self.feedback_label)

    def check_guess(self, instance):
        global player_turn, secret_number, player_scores

        # Get the player's guess
        try:
            guess = int(self.guess_input.text)
        except ValueError:
            self.feedback_label.text = "Please enter a valid number."
            return

        # Check the guess
        if guess == secret_number:
            player_scores[player_turn] += 1
            self.feedback_label.text = f"Player {player_turn} guessed it! 🎉"
            secret_number = randint(1, 100)  # Reset secret number for the next round
        elif guess < secret_number:
            self.feedback_label.text = "Too low!"
        else:
            self.feedback_label.text = "Too high!"

        # Switch turn
        player_turn = 2 if player_turn == 1 else 1
        self.instructions_label.text = f"Player {player_turn}, guess the number (1-100):"
        self.guess_input.text = ""  # Clear the input field

        # Display scores
        if guess == secret_number:
            self.instructions_label.text += f"\nScores - Player 1: {player_scores[1]}, Player 2: {player_scores[2]}"

class TwoPlayerGuessingGameApp(App):
    def build(self):
        Window.icon = "TwoPlayerGuessingGamelogo.png"
        return GuessingGame()


if __name__ == "__main__":
    TwoPlayerGuessingGameApp().run()
