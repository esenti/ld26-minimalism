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
level_complete_sound = pygame.mixer.Sound('assets/sound/level_complete.wav')
jump_sound = pygame.mixer.Sound('assets/sound/jump.wav')

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
collected = 0.0
needed = 300.0

prev_time = pygame.time.get_ticks()
initial = True

while 1:

	curr_time = pygame.time.get_ticks()
	delta = curr_time - prev_time
	prev_time = curr_time

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w and on_ground:
				jumped = 4.0
				on_ground = False
				jump_sound.play()

	dir_x = 0.3 * delta * (int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a]))
	dir_y = 0.2 * delta * (2 - jumped if int(2 - jumped) != 0 else 2)
	jumped = max(jumped - (0.1 * delta * 0.025), 0.0)


	on_ground = False
	for obj in objects:
		if player_rect.bottom > (obj.pos.y - dir_y) and player_rect.bottom <= obj.rect.top and player_rect.right > (obj.pos.x - dir_x) and player_rect.left < (obj.pos.x - dir_x + obj.rect.width):
			dir_y = 0
			on_ground = True

		if (((player_rect.left < (obj.pos.x - dir_x + obj.rect.width) and player_rect.right > (obj.pos.x - dir_x)) or (player_rect.left < (obj.pos.x - dir_x + obj.rect.width and player_rect.right > (obj.pos.x - dir_x)))) and (player_rect.top < int(obj.pos.y - dir_y + obj.rect.height) and player_rect.bottom > int(obj.pos.y - dir_y))):
			dir_x = 0

	for i in items:
		move = True
		if player_rect.colliderect(i.rect):
			if i.type == 'consumable':
				items.remove(i)
				collected += 100.0
				collect_sound.play()
				move = False
				initial = False
			elif i.type == 'exit' and i.available <= stage:
				print 'Gz!'
				level_complete_sound.play()
			elif i.type == 'jump' and i.available <= stage and on_ground:
				jumped = 5.0
				on_ground = False
				jump_sound.play()

		if move:
			i.move(-dir_x, -dir_y)

	for obj in objects:
		obj.move(-dir_x, -dir_y)


	bg_x -= 0.2 * dir_x
	bg_y -= 0.2 * dir_y
	background_rect.x = bg_x
	background_rect.y = bg_y

	if collected >= needed:
		stage += 1
		collected = collected - needed
	elif collected < 0:
		stage -= 1
		collected = needed + collected

	if not initial:
		collected -= delta * 0.01


	# Drawing
	screen.fill(bg_color)
	screen.blit(background, background_rect)
	screen.blit(player, player_rect)

	for o in objects:
		screen.blit(o.sprites[stage - 1], o.rect)

	for i in items:
		screen.blit(i.sprites[stage - 1], i.rect)

	# Progress bar
	pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 10, 620, 20))
	w = (float(collected) / float(needed)) * (width - 28)
	if w:
		pygame.draw.rect(screen, (220, 220, 220), pygame.Rect(14, 14, w, 12))

	pygame.display.flip()
