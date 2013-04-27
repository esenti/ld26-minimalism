#!/usr/bin/env python

import pygame
import sys
import loader

pygame.init()

size = width, height = 640, 480
speed = [2, 2]
bg_color = 200, 200, 200

pygame.display.set_caption('LD26 - Minimalism')
screen = pygame.display.set_mode(size)

player = pygame.transform.scale(pygame.image.load("assets/img/player_1.png"), (36, 80))
player_rect = player.get_rect();
player_rect.midbottom = (320, 420)

jumped = 0.0

objects, items = loader.load('first')

stage = 1
eaten = 0
needed = 3

while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w and on_ground:
				jumped = 3.0
				on_ground = False

	dir_x = int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a])
	dir_y = 1 - jumped if int(1 - jumped) != 0 else 1
	jumped = max(jumped - 0.01, 0.0)

	for o in objects:
		if player_rect.bottom + dir_y > o[1].top and player_rect.bottom <= o[1].top and player_rect.right > o[1].left and player_rect.left < o[1].right:
			dir_y = 0
			on_ground = True

	for i in items:
		if player_rect.colliderect(i[1]):
			items.remove(i)
			eaten += 1
		else:
			i[1].move_ip(-dir_x, -dir_y)

	for o in objects:
		o[1].move_ip(-dir_x, -dir_y)


	if eaten == needed:
		stage += 1
		eaten = 0

	# Drawing
	screen.fill(bg_color)
	screen.blit(player, player_rect)

	for o in objects:
		screen.blit(o[0][stage - 1], o[1])

	for i in items:
		screen.blit(i[0][stage - 1], i[1])

	pygame.display.flip()
