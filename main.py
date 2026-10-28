from turtle import color

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            speedup = 1.1
            speeduplateral = 0.6 # vitesse latérale de la balle après le rebond sur la raquette
            offset = ball.center_y - self.center_y
            vx, vy = ball.velocity
            nouvelle_vx =  -vx * speeduplateral
            nouvelle_vy = vy + (offset * 0.20)
            ball.velocity = (nouvelle_vx, nouvelle_vy)


class PongBall(Widget):
    velocity_x = NumericProperty(0) #vitesse de la balle en x initialisée à 0
    velocity_y = NumericProperty(0) #vitesse de la balle en y initialisée à 0
    velocity = ReferenceListProperty(velocity_x, velocity_y) #relie la velocité en x et y pour former un vecteur de vitesse

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos #vitesse de la balle + position de la balle pour obtenir la nouvelle position de la balle


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt): # dt : le temps écoulé depuis la dernière image
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went off to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))

        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

        if self.player1.score >= 5:
            print("P1 gagne")
            self.reset_game()

        elif self.player2.score >= 5:
            print("P2 gagne")
            self.reset_game()

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def reset_game(self):
        # Remet les scores à 0
        self.player1.score = 0
        self.player2.score = 0


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 120.0) # 120 images/s (fps)
        return game # On renvoie l'objet jeu pour qu'il s'affiche à l'écran
#schedule_interval demande à Kivy d'exécuter une fonction en boucle, à un intervalle régulier

if __name__ == '__main__':
    PongApp().run()