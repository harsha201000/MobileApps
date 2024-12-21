from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from random import randint


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1
            # Normalize the velocity and scale it to ensure the ball doesn't get too fast
            velocity = Vector(*ball.velocity)  # Convert ReferenceListProperty to Vector
            ball.velocity = velocity.normalize() * max(4, min(10, velocity.length()))  # Adjust the speed
            if ball.bounce_sound:
                ball.bounce_sound.play()


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # Load sound
    bounce_sound = SoundLoader.load("bounce.wav")  # Replace with your bounce sound file

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    chances = NumericProperty(10)  # Total chances before Game Over
    game_over = StringProperty("")  # Game Over message

    def serve_ball(self):
        self.ball.velocity = Vector(4, 0).rotate(randint(-45, 45))

    def update(self, dt):
        # End game if chances are 0
        if self.chances <= 0:
            self.game_over = "Game Over!"
            self.ball.velocity = (0, 0)  # Stop the ball
            return

        self.ball.move()

        # Bounce off top and bottom (no chance decrease here)
        if self.ball.y < 0 or self.ball.y > self.height - self.ball.height:
            self.ball.velocity_y *= -1
            if self.ball.bounce_sound:
                self.ball.bounce_sound.play()

        # Bounce off left and right edges and decrease chances
        if self.ball.x < 0:  # Ball hits the left edge
            self.ball.velocity_x *= -1
            self.player1.score += 1
            self.chances -= 1  # Decrease chances
            if self.ball.bounce_sound:
                self.ball.bounce_sound.play()
        elif self.ball.x > self.width - self.ball.width:  # Ball hits the right edge
            self.ball.velocity_x *= -1
            self.player2.score += 1
            self.chances -= 1  # Decrease chances
            if self.ball.bounce_sound:
                self.ball.bounce_sound.play()

        # Paddle collision
        if self.player1.bounce_ball(self.ball) or self.player2.bounce_ball(self.ball):
            self.chances -= 1  # Decrease chances when the ball hits a paddle

    def on_touch_move(self, touch):
        if touch.x < self.width / 4:
            self.player1.center_y = touch.y
        elif touch.x > self.width * 3 / 4:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        self.icon = "pong-app.png"
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    PongApp().run()
