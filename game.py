import pygame

import loader

class Game(object):
	def __init__(self, manager):

		self.manager = manager

		self.collect_sound = pygame.mixer.Sound('assets/sound/collect.wav')
		self.level_complete_sound = pygame.mixer.Sound('assets/sound/level_complete.wav')
		self.jump_sound = pygame.mixer.Sound('assets/sound/jump.wav')
		self.jump2_sound = pygame.mixer.Sound('assets/sound/jump2.wav')
		self.stage_up_sound = pygame.mixer.Sound('assets/sound/stage_up.wav')
		self.stage_down_sound = pygame.mixer.Sound('assets/sound/stage_down.wav')

		self.player = pygame.transform.scale(pygame.image.load("assets/img/player_1.png"), (36, 80))
		self.player_rect = self.player.get_rect();

		self.background = pygame.image.load("assets/img/background.png")
		self.background_rect = self.background.get_rect()

		# self.levels = ['first', 'second', 'third']
		self.levels = ['third']

		self.objects, self.items = loader.load(self.levels[0])

		self.active = False



	def enter(self, level=0):
		self.level = level
		self.objects, self.items = loader.load(self.levels[self.level])

		self.active = True
		self.bg_x = self.background_rect.x = -500
		self.bg_y = self.background_rect.y = -500
		self.player_rect.midbottom = (320, 400)
		self.jumped = 0.0
		self.stage = 1
		self.collected = 0.0
		self.needed = 300.0
		self.initial = True


	def leave(self):
		self.active = False


	def update(self, delta):
		if self.active:
			self.dir_x = 0.3 * delta * (int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a]))
			self.dir_y = 0.2 * delta * (2 - self.jumped if int(2 - self.jumped) != 0 else 2)
			self.jumped = max(self.jumped - (0.1 * delta * 0.025), 0.0)


			self.on_ground = False
			for obj in self.objects:
				if self.player_rect.bottom > (obj.pos.y - self.dir_y) and self.player_rect.bottom <= obj.rect.top and self.player_rect.right > (obj.pos.x - self.dir_x) and self.player_rect.left < (obj.pos.x - self.dir_x + obj.rect.width):
					self.dir_y = 0
					self.on_ground = True

				if (((self.player_rect.left < (obj.pos.x - self.dir_x + obj.rect.width) and self.player_rect.right > (obj.pos.x - self.dir_x)) or (self.player_rect.left < (obj.pos.x - self.dir_x + obj.rect.width and self.player_rect.right > (obj.pos.x - self.dir_x)))) and (self.player_rect.top < int(obj.pos.y - self.dir_y + obj.rect.height) and self.player_rect.bottom > int(obj.pos.y - self.dir_y))):
					self.dir_x = 0

			for i in self.items:
				move = True
				if self.player_rect.colliderect(i.rect):
					if i.type == 'consumable':
						self.items.remove(i)
						self.collected += 120.0
						self.collect_sound.play()
						move = False
						self.initial = False
					elif i.type == 'exit' and i.available <= self.stage:
						self.level_complete_sound.play()
						if self.level + 1 < len(self.levels):
							self.enter(self.level + 1)
						else:
							self.manager.set_scene('won')
					elif i.type == 'jump' and i.available <= self.stage and self.on_ground:
						self.jumped = 5.0
						self.on_ground = False
						self.jump2_sound.play()

				if move:
					i.move(-self.dir_x, -self.dir_y)

			for obj in self.objects:
				obj.move(-self.dir_x, -self.dir_y)


			self.bg_x -= 0.2 * self.dir_x
			self.bg_y -= 0.2 * self.dir_y
			self.background_rect.x = self.bg_x
			self.background_rect.y = self.bg_y

			if self.collected >= self.needed:
				self.stage_up_sound.play()
				self.stage += 1
				self.collected = self.collected - self.needed
			elif self.collected < 0:
				if self.stage > 1:
					self.stage_down_sound.play()
					self.stage -= 1
				self.collected = self.needed + self.collected

			if not self.initial:
				self.collected -= delta * 0.015


	def draw(self, screen):
		if self.active:
			screen.blit(self.background, self.background_rect)
			screen.blit(self.player, self.player_rect)

			for o in self.objects:
				screen.blit(o.sprites[self.stage - 1], o.rect)

			for i in self.items:
				screen.blit(i.sprites[self.stage - 1], i.rect)

			# Progress bar
			width = 640
			pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 10, 620, 20))
			w = (float(self.collected) / float(self.needed)) * (width - 28)
			if w:
				pygame.draw.rect(screen, (220, 220, 220), pygame.Rect(14, 14, w, 12))


	def event(self, event):
		if self.active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w and self.on_ground:
					self.jumped = 4.0
					self.on_ground = False
					self.jump_sound.play()
				elif event.key == pygame.K_r:
					self.objects, self.items = loader.load(self.levels[self.level])
					self.enter(self.level)
				elif event.key == pygame.K_ESCAPE:
					self.manager.set_scene('menu')
