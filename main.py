import kivy 
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
kivy.require('1.9.1') # replace with your current kivy version !
# sinov uchun
from kivy.app import App
from kivy.uix.label import Label
from kivy import Config
Config.set('graphics', 'multisamples', '0')
###################

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class PongPaddle(Widget):
	score = NumericProperty(0)
	def bounce_ball(self,ball):
		if self.collide_widget(ball):
			vx , vy = ball.velocity
			offset = (ball.center_y - self.center_y) / (self.height / 2)
			bounced = Vector(-1 * vx , vy)
			vel = bounced * 1.1
			ball.velocity = vel.x , vel.y + offset

class PongBall(Widget):
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)

	velocity = ReferenceListProperty(velocity_x , velocity_y)
	def move(self):
		self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)
	def serve_ball(self,vel = (4,0)):
		self.ball.center = self.center
		self.ball.velocity = Vector(vel[0] , vel[1]).rotate(randint(0,360))

	def update(self, dt):
		self.ball.move()

		self.player1.bounce_ball(self.ball)
		self.player2.bounce_ball(self.ball)
		if self.ball.y < 0 or self.ball.top > self.height:
			self.ball.velocity_y *= -1 
		if self.ball.x < self.x:
		    # Первый игрок проиграл, добавляем 1 очко второму игроку
		    self.player2.score += 1
		    self.serve_ball(vel=(4,0)) # заново спавним шарик в центре

		if self.ball.x > self.width:
		    # Второй игрок проиграл, добавляем 1 очко первому игроку
		    self.player1.score += 1
		    self.serve_ball(vel=(-4,0))
	def on_touch_move(self, touch):
	    # первый игрок может касаться только своей части экрана (левой)
	    if touch.x < self.width / 3:
	        self.player1.center_y = touch.y

	    # второй игрок может касаться только своей части экрана (правой)
	    if touch.x > self.width - self.width / 3:
	        self.player2.center_y = touch.y	



class PongApp(App):    
	def build(self):
		game  = PongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update, 1.0/60)
		return game
if __name__ == '__main__':
	PongApp().run()
