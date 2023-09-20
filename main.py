import pygame
from pygame.locals import *


pygame.init()

screen_x = 700
screen_y = 500
screen = pygame.display.set_mode((screen_x, screen_y))
screen_bg = (100, 100, 100)

clock = pygame.time.Clock()
fps = 10

cobrinha = {"cor": [255, 255, 255], "pos": [[x, 30] for x in range(1000, 20, -10)], "tamanho": 10, "design": 1}
movimentos = {K_a: [0, -1, K_d], K_d: [0, 1, K_a], K_w: [1, -1, K_s], K_s: [1, 1, K_w]}
sentido_da_cobrinha = 0 # Gerencia em qual eixo a cobrinha vai se deslocar. 0=x, 1=y
movimento_da_cobrinha = 1 # Gerencia se ela vai se movimentar para baixo/cima ou esquerda/direita.
antigo_movimento_da_cobrinha = 0


run = True
while run:
	clock.tick(fps)
	for event in pygame.event.get():
		if event.type == QUIT:
			run = False
		if event.type == KEYDOWN:
			tecla = event.key
			if tecla in movimentos:
				# Define o movimento e o sentido com base na tecla pressionada
				if tecla == K_a and antigo_movimento_da_cobrinha == K_d:
					continue
				elif tecla == K_d and antigo_movimento_da_cobrinha == K_a:
					continue
				elif tecla == K_s and antigo_movimento_da_cobrinha == K_w:
					continue
				elif tecla == K_w and antigo_movimento_da_cobrinha == K_s:
					continue	
				sentido_da_cobrinha = movimentos[tecla][0]
				movimento_da_cobrinha = movimentos[tecla][1]
				antigo_movimento_da_cobrinha = tecla



	# Salva a posicão antiga da cabeça da cobrinha
	cabeca_da_cobrinha = cobrinha["pos"][0][:]
	cobrinha["pos"][0][sentido_da_cobrinha] += movimento_da_cobrinha*10
	if cobrinha["pos"][0][0] > screen_x:
		cobrinha["pos"][0][0] = 0
	if cobrinha["pos"][0][1] > screen_y:
		cobrinha["pos"][0][1] = 0
	if cobrinha["pos"][0][0] < 0:
		cobrinha["pos"][0][0] = screen_x
	if cobrinha["pos"][0][1] < 0:
		cobrinha["pos"][0][1] = screen_y

	screen.fill(screen_bg)

	# Atualioza o restante do corpo da cobrinha
	for n_parte_da_cobrinha in range(1, len(cobrinha["pos"])):
		posicao_atual = cobrinha["pos"][n_parte_da_cobrinha][:]
		cobrinha["pos"][n_parte_da_cobrinha] = cabeca_da_cobrinha
		cabeca_da_cobrinha = posicao_atual
		

	# Desenha a cobrinha na tela
	for parte_da_cobrinha in cobrinha["pos"]:
		x_pos = parte_da_cobrinha[0]
		y_pos = parte_da_cobrinha[1]
		tamanho = cobrinha["tamanho"] - cobrinha["design"]
		pygame.draw.rect(screen, cobrinha["cor"], (x_pos, y_pos, tamanho, tamanho))

	pygame.display.update()


pygame.quit()
