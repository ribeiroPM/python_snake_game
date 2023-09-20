import pygame
from pygame.locals import *


pygame.init()

screen = pygame.display.set_mode((400, 400))

run = True
while run:
	for event in pygame.event.get():
		if event.type == QUIT:
			run = False


	pygame.display.update()


pygame.quit()
