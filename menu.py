import pygame
import sys


class Menu(object):

	def __init__(self, manager):

		self.manager = manager

		self.background = pygame.image.load("assets/img/menu/background.png")
		self.background_rect = self.background.get_rect()

		self.start = pygame.image.load("assets/img/menu/start.png")
		self.start_rect = self.start.get_rect()
		self.start_rect.center = (320, 360)

		self.quit = pygame.image.load("assets/img/menu/quit.png")
		self.quit_rect = self.quit.get_rect()
		self.quit_rect.center = (320, 420)

		self.hl = pygame.image.load("assets/img/menu/hl.png")
		self.hl_rect = self.hl.get_rect()
		self.hl_rect.center = (320, 360)

		self.sound = pygame.mixer.Sound('assets/sound/menu.wav')

		self.active = False

	def enter(self):
		self.highlighted = 0
		self.active = True

	def leave(self):
		self.active = False

	def update(self, delta):
		pass

	def draw(self, screen):

		if self.active:
			screen.blit(self.background, self.background_rect)

			screen.blit(self.hl, self.hl_rect)
			screen.blit(self.start, self.start_rect)
			screen.blit(self.quit, self.quit_rect)

	def event(self, event):
		if self.active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w and self.highlighted == 1:
					self.highlighted = 0
					self.hl_rect.center = (320, 360)
					self.sound.play()
				elif event.key == pygame.K_s and self.highlighted == 0:
					self.highlighted = 1
					self.hl_rect.center = (320, 420)
					self.sound.play()
				elif event.key == pygame.K_SPACE:
					if self.highlighted == 0:
						self.manager.set_scene('info')
					if self.highlighted == 1:
						sys.exit()

					return True


class Info(object):

	def __init__(self, manager):

		self.manager = manager

		self.background = pygame.image.load("assets/img/menu/info.png")
		self.background_rect = self.background.get_rect()


		self.sound = pygame.mixer.Sound('assets/sound/menu.wav')

		self.active = False

	def enter(self):
		self.active = True

	def leave(self):
		self.active = False

	def update(self, delta):
		pass

	def draw(self, screen):

		if self.active:
			screen.blit(self.background, self.background_rect)

	def event(self, event):
		if self.active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.manager.set_scene('game')


class Won(object):

	def __init__(self, manager):

		self.manager = manager

		self.background = pygame.image.load("assets/img/menu/won.png")
		self.background_rect = self.background.get_rect()


		self.sound = pygame.mixer.Sound('assets/sound/menu.wav')

		self.active = False

	def enter(self):
		self.active = True

	def leave(self):
		self.active = False

	def update(self, delta):
		pass

	def draw(self, screen):

		if self.active:
			screen.blit(self.background, self.background_rect)

	def event(self, event):
		if self.active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.manager.set_scene('menu')

					return True





