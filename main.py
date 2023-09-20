import pygame
from pygame.locals import *


pygame.init()

screen = pygame.display.set_mode((400, 400))
screen_bg = (100, 100, 100)

clock = pygame.time.Clock()
fps = 30

cobrinha = {"cor": [255, 255, 255], "pos": [[x, 30] for x in range(60, 20, -10)]}
movimentos = {K_a: [0, -1], K_d: [0, 1], K_w: [1, -1], K_s: [1, 1]}
sentido_da_cobrinha = 0 # Gerencia em qual eixo a cobrinha vai se deslocar.
movimento_da_cobrinha = 1 # Gerencia se ela vai se movimentar para baixo/cima ou esquerda/direita


run = True
while run:
	clock.tick(fps)
	for event in pygame.event.get():
		if event.type == QUIT:
			run = False
		if event.type == KEYDOWN:
			tecla = event.key
			if tecla in movimentos:
				sentido_da_cobrinha = movimentos[tecla][0]
				movimento_da_cobrinha = movimentos[tecla][1]

	cabeca_da_cobrinha = cobrinha["pos"][0][:]
	cobrinha["pos"][0][sentido_da_cobrinha] += movimento_da_cobrinha*5

	screen.fill(screen_bg)

	for parte_da_cobrinha in cobrinha["pos"]:
		x_pos = parte_da_cobrinha[0]
		y_pos = parte_da_cobrinha[1]
		pygame.draw.rect(screen, cobrinha["cor"], (x_pos, y_pos, 10, 10))
	pygame.display.update()


pygame.quit()
