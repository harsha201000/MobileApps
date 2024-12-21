from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from kivy.utils import platform
import os

class DoodleCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_color = (1, 0, 0)  # Default color is red
        self.line_width = 5

    def on_touch_down(self, touch):
        # Start drawing a circle at the touch point
        with self.canvas:
            Color(*self.current_color)
            d = self.line_width
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud["line"] = Line(points=(touch.x, touch.y), width=self.line_width)

    def on_touch_move(self, touch):
        # Continue drawing lines
        if "line" in touch.ud:
            touch.ud["line"].points += [touch.x, touch.y]

    def set_color(self, color):
        # Change the current drawing color
        self.current_color = color

    def save_canvas(self):
        # Save the canvas as an image
        screenshot_path = "doodle.png"
        self.export_to_png(screenshot_path)
        print(f"Screenshot saved as {screenshot_path}")
        
    def clear_canvas(self):
        # Clear all drawing instructions
        self.canvas.clear()  # This clears the canvas drawing
        print("Canvas cleared!")


class DoodleApp(App):
    def build(self):
        Window.set_icon('digitaldoodlelogo.png')
        
        root = BoxLayout(orientation="vertical")
        

        # Doodle Canvas
        self.canvas_widget = DoodleCanvas()
        root.add_widget(self.canvas_widget)

        # Button Layout
        button_layout = BoxLayout(size_hint=(1, 0.2))

        # Color Buttons
        colors = {"Red": (1, 0, 0), "Green": (0, 1, 0), "Blue": (0, 0, 1), "Yellow": (1, 1, 0), "Orange": (1, 0.49, 0), "Purple": (0.459,0,0.459), "Pink": (1,0.008,1), "White": (1,1,1), "Gray": (0.49,0.463,0.463)}
        for color_name, color_value in colors.items():
            btn = Button(text=color_name, background_color=color_value + (1,))
            btn.bind(on_press=lambda instance, clr=color_value: self.canvas_widget.set_color(clr))
            button_layout.add_widget(btn)

        # Take Picture Button
        take_pic_button = Button(text="Take Photo", background_color=(1, 1, 0, 1))
        take_pic_button.bind(on_press=lambda instance: self.canvas_widget.save_canvas())
        button_layout.add_widget(take_pic_button)
        
        # Clear Button
        clear_button = Button(text="Clear", background_color=(1, 0, 0, 1))
        clear_button.bind(on_press=lambda instance: self.canvas_widget.clear_canvas())
        button_layout.add_widget(clear_button)

        root.add_widget(button_layout)
        return root


if __name__ == "__main__":
    DoodleApp().run()
