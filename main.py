import pygame
from pygame.locals import *
from cobra import Cobra
from time import strftime
a = 0
s = strftime("%S")
def contar_fps():
	global s, a
	if s != strftime("%S"):
		s = strftime("%S")
		print(a)
		a = 0



# Constantes referentes a janela do jogo
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SCREEN_COLOR = (255, 255, 255)

pygame.init()
# Inicia uma janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Definições para o tempo de atualização da tela
# clock = pygame.time.Clock()
# fps = 10
limite_atualizacao_tela = 150000
contador_atualizacao = 0
# Instancia a cobrinha
cobra_1 = Cobra()
cobra_2 = Cobra(tamanho=10, pos_y=100)
cobra_3 = Cobra(tamanho=100, pos_y=200)
cobra_4 = Cobra(tamanho=15, pos_y=300)

# Mostra todas as informacoes da cobra
show_infos = False
# pausa
pause = False


run = True
while run:
	# Controle de atualizações por segundo
	# clock.tick(fps)
	# Laço de eventos de entrada (teclado/mouse)
	for event in pygame.event.get():
		# Verifica se o [x] da janela foi clicado
		if event.type == QUIT:
			run = False
		if event.type == KEYDOWN:
			key = event.key
			if key == K_a:
				cobra_1.para_esquerda()
			elif key == K_d:
				cobra_1.para_direita()
			elif key == K_w:
				cobra_1.para_cima()
			elif key == K_s:
				cobra_1.para_baixo()
			elif key == K_SPACE:
				pause = False if pause == True else True
			elif key == K_q:
				show_infos = False if show_infos == True else True
			elif key == K_p:
				cobra_1.tamanho += 1
	if not pause:
		if contador_atualizacao == limite_atualizacao_tela:
			# Reseta a tela para a cor inicial
			screen.fill(SCREEN_COLOR)
			cobra_1.update(screen)

			cobra_2.update(screen)
			cobra_3.update(screen)
			cobra_4.update(screen)

			if not cobra_1.estado:
				run = False
			contador_atualizacao = 0
			if show_infos:
				cobra_1.get_infos(screen)
			""" # Bloco para contar quantas atualizações estamos tendo da cobrinha
			a+=1
			contar_fps() 
			"""
			# Atualiza a tela para aplicar possiveis alterações
			pygame.display.update()
			
		else:
			contador_atualizacao += 1


pygame.quit()

