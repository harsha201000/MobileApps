import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from plyer import accelerometer
from kivy.uix.image import Image
from kivy.uix.button import Button
import platform
from kivy.core.window import Window
import os

class HappyAccelerometerApp(App):
    def build(self):
        # Set the window icon
        icon_path = "happyaccelerometerlogo.png"  # Replace with your icon file path
        if os.path.exists(icon_path):  # Check if the icon file exists
            Window.set_icon(icon_path)
        
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        
        # Display accelerometer data
        self.accel_label = Label(text="Accelerometer Data: [0, 0, 0]", font_size=20)
        self.layout.add_widget(self.accel_label)

        # Happy Image or Message
        self.happy_label = Label(text="Keep Moving!", font_size=30, bold=True, color=(0, 1, 0, 1))
        self.happy_image = Image(source="happy_face.png")  # Replace with your image path
        self.layout.add_widget(self.happy_label)
        self.layout.add_widget(self.happy_image)

        # Reset Button
        self.reset_button = Button(text="Reset", size_hint=(1, 0.2))
        self.reset_button.bind(on_press=self.reset_happy_message)
        self.layout.add_widget(self.reset_button)

        # Only try to enable the accelerometer if the platform supports it
        if platform.system() != 'Windows':
            try:
                accelerometer.enable()
                Clock.schedule_interval(self.update_accelerometer_data, 0.1)
            except NotImplementedError:
                self.accel_label.text = "Accelerometer not supported on this device"
        else:
            # Simulate accelerometer on Windows
            self.accel_label.text = "Simulated Accelerometer Data"
            Clock.schedule_interval(self.simulate_accelerometer_data, 0.1)

        return self.layout

    def update_accelerometer_data(self, dt):
        try:
            accel_data = accelerometer.acceleration
            if accel_data:
                x, y, z = accel_data
                self.accel_label.text = f"Accelerometer Data: [x={x:.2f}, y={y:.2f}, z={z:.2f}]"

                # Check for significant movement (e.g., shaking or tilting)
                if abs(x) > 15 or abs(y) > 15 or abs(z) > 15:
                    self.happy_label.text = "You're Awesome! 🎉"
                    self.happy_label.color = (1, 0, 0, 1)  # Change color to red
                    self.happy_image.source = "happy_face.png"  # Ensure the image reflects happiness
        except Exception as e:
            self.accel_label.text = f"Error reading accelerometer: {e}"

    def simulate_accelerometer_data(self, dt):
        # Simulate random accelerometer data for testing on Windows
        x, y, z = random.uniform(-20, 20), random.uniform(-20, 20), random.uniform(-20, 20)
        self.accel_label.text = f"Accelerometer Data: [x={x:.2f}, y={y:.2f}, z={z:.2f}]"

        # Simulate significant movement (e.g., shaking or tilting)
        if abs(x) > 15 or abs(y) > 15 or abs(z) > 15:
            self.happy_label.text = "You're Awesome! 🎉"
            self.happy_label.color = (1, 0, 0, 1)  # Change color to red
            self.happy_image.source = "happy_face.png"  # Ensure the image reflects happiness

    def reset_happy_message(self, instance):
        self.happy_label.text = "Keep Moving!"
        self.happy_label.color = (0, 1, 0, 1)  # Reset color to green
        self.happy_image.source = "neutral_face.png"  # Reset image to neutral state


if __name__ == "__main__":
    HappyAccelerometerApp().run()
