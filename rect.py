#!/usr/bin/env python

import pygame
import sys
import loader
from scene import SceneManager

pygame.init()
pygame.mixer.init(frequency=44100, channels=1)

size = width, height = 640, 480
speed = [2, 2]
bg_color = 255, 255, 0

pygame.display.set_caption('LD26 - Minimalism')
screen = pygame.display.set_mode(size)

prev_time = pygame.time.get_ticks()

manager = SceneManager()
manager.set_scene('menu')

while 1:

	curr_time = pygame.time.get_ticks()
	delta = curr_time - prev_time
	prev_time = curr_time

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		else:
			manager.event(event)

	manager.update(delta)

	# Drawing
	screen.fill(bg_color)
	manager.draw(screen)

	pygame.display.flip()
