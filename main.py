#!/usr/bin/env python

import pygame
import sys
import loader

pygame.init()
pygame.mixer.init(frequency=44100, channels=1)

size = width, height = 640, 480
speed = [2, 2]
bg_color = 200, 200, 200

pygame.display.set_caption('LD26 - Minimalism')
screen = pygame.display.set_mode(size)

collect_sound = pygame.mixer.Sound('assets/sound/collect.wav')

player = pygame.transform.scale(pygame.image.load("assets/img/player_1.png"), (36, 80))
player_rect = player.get_rect();
player_rect.midbottom = (320, 420)

background = pygame.image.load("assets/img/background.png")
background_rect = background.get_rect()
bg_x = background_rect.x
bg_y = background_rect.y

jumped = 0.0

objects, items = loader.load('first')

stage = 1
eaten = 0
needed = 3

prev_time = pygame.time.get_ticks()

while 1:

	curr_time = pygame.time.get_ticks()
	delta = curr_time - prev_time
	prev_time = curr_time

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w and on_ground:
				jumped = 3.0
				on_ground = False

	dir_x = 0.2 * delta * (int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a]))
	dir_y = 0.2 * delta * (1 - jumped if int(1 - jumped) != 0 else 1)
	jumped = max(jumped - 0.02, 0.0)

	for o in objects:
		if player_rect.bottom + dir_y > o[1].top and player_rect.bottom <= o[1].top and player_rect.right > o[1].left and player_rect.left < o[1].right:
			dir_y = 0
			on_ground = True

	for i in items:
		if player_rect.colliderect(i[1]):
			items.remove(i)
			eaten += 1
			collect_sound.play()
		else:
			i[2][0] -= dir_x
			i[2][1] -= dir_y
			i[1].x = i[2][0]
			i[1].y = i[2][1]

	for o in objects:
		o[2][0] -= dir_x
		o[2][1] -= dir_y
		o[1].x = o[2][0]
		o[1].y = o[2][1]


	bg_x -= 0.2 * dir_x
	bg_y -= 0.2 * dir_y
	background_rect.x = bg_x
	background_rect.y = bg_y

	if eaten == needed:
		stage += 1
		eaten = 0

	# Drawing
	screen.fill(bg_color)
	screen.blit(background, background_rect)
	screen.blit(player, player_rect)

	for o in objects:
		screen.blit(o[0][stage - 1], o[1])

	for i in items:
		screen.blit(i[0][stage - 1], i[1])

	pygame.display.flip()
