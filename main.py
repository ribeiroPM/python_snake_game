import pygame
from pygame.locals import *
from random import randint

# O jogo ainda esta em processo de desenvolvimento, atualizacoes em breve


pygame.init()

screen_x = 700
screen_y = 500
screen = pygame.display.set_mode((screen_x, screen_y))
screen_bg = (100, 100, 100)

clock = pygame.time.Clock()
fps = 20

# Variaveis a respeito da cobrinha
cobrinha = {"cores": [[255, 255, 255], [255, 0, 255]], "pos": [[x, 30] for x in range(50, 20, -10)], "tamanho": 10, "design": 1}
movimentos = {K_a: [0, -1], K_d: [0, 1], K_w: [1, -1], K_s: [1, 1]}
sentido_da_cobrinha = 0 # Gerencia em qual eixo a cobrinha vai se deslocar. 0=x, 1=y
movimento_da_cobrinha = 1 # Gerencia se ela vai se movimentar para baixo/cima ou esquerda/direita.
antigo_movimento_da_cobrinha = 0

# Variaveis a respeito da frutinha
def gera_fruta_nova():
	return (randint(0, (screen_x-1)//10)*10, randint(0, (screen_y-1)//10)*10)
fruta = {"tem_fruta": True, "pos": gera_fruta_nova(), "cor": [255, 0, 0]}
print(fruta["pos"])



def teve_colisao(ponto_a, ponto_b):
	ponto = pygame.draw.rect(screen, (0, 0, 0), (ponto_a[0], ponto_a[1], 1, 1))
	if ponto.collidepoint(ponto_b[0], ponto_b[1]):
		return True

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
					# Cadeia de if's responsáveis por evitar movimentos "para trás", que resultariam em game_over
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

	# Verifica se a cobrinha atingiu os limites da tela
	if cobrinha["pos"][0][0] > screen_x:
		cobrinha["pos"][0][0] = 0
	if cobrinha["pos"][0][1] > screen_y:
		cobrinha["pos"][0][1] = 0
	if cobrinha["pos"][0][0] < 0:
		cobrinha["pos"][0][0] = screen_x
	if cobrinha["pos"][0][1] < 0:
		cobrinha["pos"][0][1] = screen_y

	screen.fill(screen_bg)

	# Atualiza o restante do corpo da cobrinha
	for n_parte_da_cobrinha in range(1, len(cobrinha["pos"])):
		posicao_atual = cobrinha["pos"][n_parte_da_cobrinha][:]
		cobrinha["pos"][n_parte_da_cobrinha] = cabeca_da_cobrinha
		cabeca_da_cobrinha = posicao_atual
		

	# Desenha a cobrinha na tela
	for numero_da_parte, parte_da_cobrinha in enumerate(cobrinha["pos"]):
		x_pos = parte_da_cobrinha[0]
		y_pos = parte_da_cobrinha[1]
		tamanho = cobrinha["tamanho"] - cobrinha["design"]
		cor = cobrinha["cores"][0] if numero_da_parte != 0 else cobrinha["cores"][1]
		pygame.draw.rect(screen, cor, (x_pos, y_pos, tamanho, tamanho))
		if teve_colisao(cobrinha["pos"][0], parte_da_cobrinha) and numero_da_parte > 0:
			run = False


	# Desenha a fruta na tela
	fruta_pos_x = fruta["pos"][0]
	fruta_pos_y = fruta["pos"][1]
	pygame.draw.rect(screen, fruta["cor"], (fruta_pos_x, fruta_pos_y, 10, 10))

	if teve_colisao(cobrinha["pos"][0], fruta["pos"]):
		fruta["pos"] = gera_fruta_nova()
		cobrinha["pos"].append([0, 0])
		print(fruta["pos"])


	pygame.display.update()


pygame.quit()
