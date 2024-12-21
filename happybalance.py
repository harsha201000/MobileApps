from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import random


class HappyBalanceGame(BoxLayout):
    balance = NumericProperty(50)  # Initial balance value
    status_message = StringProperty("Keep the balance!")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Status Label
        self.status_label = Label(text=self.status_message, font_size="24sp", size_hint=(1, 0.2))
        self.add_widget(self.status_label)

        # Balance Slider
        self.slider = Slider(min=0, max=100, value=self.balance, step=1, size_hint=(1, 0.2))
        self.slider.bind(value=self.update_balance)
        self.add_widget(self.slider)

        # Happy/Sad Image
        self.face_image = Image(source="happy_face.png", size_hint=(None, None), size=(200, 200))
        self.add_widget(self.face_image)

        # Reset Button
        reset_button = Button(text="Reset", size_hint=(1, 0.2))
        reset_button.bind(on_press=self.reset_game)
        self.add_widget(reset_button)

        # Load sound effects
        self.sad_sound = SoundLoader.load("sad_sound.mp3")  # Replace with your sad sound file
        self.happy_sound = SoundLoader.load("happy_sound.mp3")  # Replace with your happy sound file

        # Periodic random balance adjustment
        Clock.schedule_interval(self.random_adjust_balance, 1)

    def update_balance(self, instance, value):
        """Update balance based on slider movement."""
        self.balance = value
        self.check_balance()

    def random_adjust_balance(self, dt):
        """Simulate external forces adjusting the balance."""
        adjustment = random.uniform(-5, 5)
        self.balance += adjustment
        self.balance = max(0, min(100, self.balance))  # Ensure balance stays within range
        self.slider.value = self.balance

    def check_balance(self):
        """Check if the balance is within the happy range."""
        if 40 <= self.balance <= 60:
            self.status_message = "You're balanced! 😊"
            self.face_image.source = "happy_face.png"
            if self.happy_sound:
                self.happy_sound.play()
        else:
            self.status_message = "Out of balance! 😟"
            self.face_image.source = "sad_face.png"
            if self.sad_sound:
                self.sad_sound.play()

        self.status_label.text = self.status_message

    def reset_game(self, instance):
        """Reset the game to the initial state."""
        self.balance = 50
        self.slider.value = self.balance
        self.status_message = "Keep the balance!"
        self.face_image.source = "happy_face.png"
        self.status_label.text = self.status_message


class HappyBalanceApp(App):
    def build(self):
        Window.icon = "happybalancechallengelogo.png"  # Set the window icon (optional)
        return HappyBalanceGame()


if __name__ == "__main__":
    HappyBalanceApp().run()
