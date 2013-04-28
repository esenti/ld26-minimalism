import imp
import pygame


class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Object(object):
	def __init__(self, sprites, rect):
		self.sprites = sprites
		self.rect = rect
		self.pos = Point(rect.x, rect.y)

	def move(self, x, y):
		self.pos.x += x
		self.pos.y += y
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y


class Item(object):
	def __init__(self, sprites, rect, t, available):
		self.sprites = sprites
		self.rect = rect
		self.pos = Point(rect.x, rect.y)
		self.type = t
		self.available = available

	def move(self, x, y):
		self.pos.x += x
		self.pos.y += y
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

def load(name):

	fp, pathname, description = imp.find_module('maps/' + name)
	level = imp.load_module('maps/' + name, fp, pathname, description)

	objects = []

	for o in level.objects:
		sprites = [pygame.image.load("assets/img/%s_%d.png" % (o['name'], num)) for num in [1, 2, 3]]
		rect = sprites[0].get_rect()

		for item in o['pos'].iteritems():
			rect.__setattr__(*item)

		objects.append(Object(sprites, rect))


	items = []
	for i in level.items:
		sprites = [pygame.image.load("assets/img/%s_%d.png" % (i['name'], num)) for num in [1, 2, 3]]
		rect = sprites[0].get_rect()

		for item in i['pos'].iteritems():
			rect.__setattr__(*item)

		items.append(Item(sprites, rect, i['type'], i.get('available', 1)))

	return objects, items
