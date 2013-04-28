from menu import Menu
from game import Game

class SceneManager(object):
	def __init__(self):
		self.menu = Menu(self)
		self.game = Game(self)


	def update(self, delta):
		self.menu.update(delta)
		self.game.update(delta)


	def event(self, event):
		self.menu.event(event)
		self.game.event(event)


	def draw(self, screen):
		self.menu.draw(screen)
		self.game.draw(screen)


	def set_scene(self, scene):
		if scene == 'menu':
			self.game.leave()
			self.menu.enter()
		elif scene == 'game':
			self.menu.leave()
			self.game.enter()
