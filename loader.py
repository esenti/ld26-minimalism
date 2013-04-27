import imp
import pygame

def load(name):

	fp, pathname, description = imp.find_module('maps/' + name)
	level = imp.load_module('maps/' + name, fp, pathname, description)

	objects = []

	for o in level.objects:
		sprites = [pygame.image.load("assets/img/%s_%d.png" % (o['name'], num)) for num in [1, 2]]
		rect = sprites[0].get_rect()

		for item in o['pos'].iteritems():
			rect.__setattr__(*item)

		objects.append((sprites, rect, [rect.x, rect.y]))


	items = []
	for i in level.items:
		sprites = [pygame.image.load("assets/img/%s_%d.png" % (i['name'], num)) for num in [1, 2]]
		rect = sprites[0].get_rect()

		for item in i['pos'].iteritems():
			rect.__setattr__(*item)

		items.append((sprites, rect, [rect.x, rect.y]))

	return objects, items
