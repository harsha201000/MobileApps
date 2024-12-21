from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from random import randint
from kivy.core.window import Window

class GuessingGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Initial setup
        self.max_attempts = 5
        self.attempts = 0
        self.secret_number = randint(1, 100)

        # Instructions Label
        self.instructions_label = Label(
            text="Guess the number (1-100):", font_size="20sp"
        )
        self.add_widget(self.instructions_label)

        # Input field for guesses
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
        """Handle the guess submitted by the player."""
        # Get the player's guess
        try:
            guess = int(self.guess_input.text)
        except ValueError:
            self.feedback_label.text = "Please enter a valid number."
            return

        # Check the guess
        if guess == self.secret_number:
            self.feedback_label.text = f"🎉 Congratulations! You guessed it right!"
            self.end_game(success=True)
        elif guess < self.secret_number:
            self.feedback_label.text = "Too low!"
        else:
            self.feedback_label.text = "Too high!"

        # Increment attempts and check if max attempts reached
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            self.end_game(success=False)

        # Clear the input field for the next attempt
        self.guess_input.text = ""

    def end_game(self, success):
        """End the game with a message and disable further guesses."""
        if success:
            self.instructions_label.text = f"Great job! You found the number in {self.attempts} attempts!"
        else:
            self.instructions_label.text = f"Game over! The correct number was {self.secret_number}."
        self.submit_button.disabled = True
        self.guess_input.disabled = True


class OnePlayerGuessingApp(App):
    def build(self):
        Window.icon = "OnePlayerGuessingGamelogo.png"
        return GuessingGame()


if __name__ == "__main__":
    OnePlayerGuessingApp().run()
    