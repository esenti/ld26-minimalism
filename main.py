#!/usr/bin/env python

import pygame
import sys
import loader

pygame.init()
pygame.mixer.init(frequency=44100, channels=1)

size = width, height = 640, 480
speed = [2, 2]
bg_color = 255, 255, 0

pygame.display.set_caption('LD26 - Minimalism')
screen = pygame.display.set_mode(size)

collect_sound = pygame.mixer.Sound('assets/sound/collect.wav')

player = pygame.transform.scale(pygame.image.load("assets/img/player_1.png"), (36, 80))
player_rect = player.get_rect();
player_rect.midbottom = (320, 400)

background = pygame.image.load("assets/img/background.png")
background_rect = background.get_rect()
bg_x = background_rect.x = -500
bg_y = background_rect.y = -500

jumped = 0.0

objects, items = loader.load('first')

stage = 1
collected = 0
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
	jumped = max(jumped - 0.1 * delta * 0.02, 0.0)

	for o in objects:
		if player_rect.bottom > (o.pos.y - dir_y) and player_rect.bottom <= o.rect.top and player_rect.right > (o.pos.x - dir_x) and player_rect.left < (o.pos.x - dir_x + o.rect.width):
			dir_y = 0
			on_ground = True

		if (((player_rect.left < (o.pos.x - dir_x + o.rect.width) and player_rect.right > (o.pos.x - dir_x)) or (player_rect.left < (o.pos.x - dir_x + o.rect.width and player_rect.right > (o.pos.x - dir_x)))) and (player_rect.top < int(o.pos.y - dir_y + o.rect.height) and player_rect.bottom > int(o.pos.y - dir_y))):
			dir_x = 0

	for i in items:
		if player_rect.colliderect(i[1]):
			items.remove(i)
			collected += 1
			collect_sound.play()
		else:
			i[2].x -= dir_x
			i[2].y -= dir_y
			i[1].x = i[2].x
			i[1].y = i[2].y

	for o in objects:
		o.move(-dir_x, -dir_y)


	bg_x -= 0.2 * dir_x
	bg_y -= 0.2 * dir_y
	background_rect.x = bg_x
	background_rect.y = bg_y

	if collected == needed:
		stage += 1
		collected = 0

	# Drawing
	screen.fill(bg_color)
	screen.blit(background, background_rect)
	screen.blit(player, player_rect)

	for o in objects:
		screen.blit(o.sprites[stage - 1], o.rect)

	for i in items:
		screen.blit(i[0][stage - 1], i[1])

	# Progress bar
	pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 10, 620, 20))
	w = (float(collected) / float(needed)) * 612
	pygame.draw.rect(screen, (220, 220, 220), pygame.Rect(14, 14, w, 12))

	pygame.display.flip()
