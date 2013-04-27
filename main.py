#!/usr/bin/env python

import pygame
import sys

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

objects = []

ground = pygame.image.load("assets/img/ground_1.png")
ground_rect = ground.get_rect()
ground_rect.bottom = 480

objects.append((ground, ground_rect))

platform = pygame.image.load("assets/img/platform_1.png")
platform_rect = platform.get_rect()
platform_rect.center = (200, 360)
objects.append((platform, platform_rect))

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


	for o in objects:
		o[1].move_ip(-dir_x, -dir_y)

	screen.fill(bg_color)

	screen.blit(player, player_rect)

	for o in objects:
		screen.blit(*o)

	pygame.display.flip()
