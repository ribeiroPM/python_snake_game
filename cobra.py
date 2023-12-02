import pygame
from pygame.locals import *
from os import system
class Cobra:
	def __init__(self, tamanho=30, pos_x=30, pos_y=30):
		self.quantidade_de_partes = 10
		self.tamanho = tamanho
		self.pos_x_inicial = pos_x
		self.pos_y_inicial = pos_y
		self.posicoes = [{"x": x+self.tamanho, "y": self.pos_y_inicial+self.tamanho, "direcao_antiga": "direita", "direcao_nova": "direita"} for x in range(self.pos_x_inicial, self.pos_x_inicial+self.quantidade_de_partes)] 
		self.cor = [233, 0, 0]
		self.cor_cabeca = [0, 233, 0]
		self.cor_rabo = [0, 0, 233]
		self.direcoes = {K_a: "esquerda", K_d: "direita", K_w: "cima", K_s: "baixo"} # 1 para direita; 2 para esquerda; 3 para cima; e 4 para "baixo"
		self.direcao = "direita"
		self.direcao_antiga = None
		self.estado = True

		# Importação e Transformação dos Sprites
		self.imagens = {"tronco": pygame.image.load("imagens/tronco.png").convert_alpha(),
						"cabeca": pygame.image.load("imagens/cabeca.png").convert_alpha(),
						"rabo": pygame.image.load("imagens/rabo.png").convert_alpha(),
						"dobrada": pygame.image.load("imagens/dobrada.png").convert_alpha(),
						"dobrada_2": pygame.image.load("imagens/dobrada_2.png").convert_alpha()
						}
		self.imagens_transformadas = {}
		
		# Define os Sprites da Cabeca 
		self.direcoes_cabeca_rabo = {"esquerda": 180, "direita": 0, "cima": 90, "baixo": -90}

		# Define se será exibido as caixas de colisão
		self.exibicao = False

	def update(self, surface):
		# Possibilita aumentar ou diminuir o tamanho dos sprites a qualquer instante
		self.imagens_transformadas = {x: pygame.transform.scale(y, (self.tamanho, self.tamanho)) for x, y in self.imagens.items()}

		# Guarda a antiga posição 0 (cabeça)
		antiga_cabeca = self.posicoes[0].copy()
		# Atualiza para a posição 0 para a direção escolhida
		if self.direcao == "esquerda":
			self.posicoes[0]["x"] -= self.tamanho
		elif self.direcao == "direita":
			self.posicoes[0]["x"] += self.tamanho
		elif self.direcao == "cima":
			self.posicoes[0]["y"] -= self.tamanho
		elif self.direcao == "baixo":
			self.posicoes[0]["y"] += self.tamanho

		# Atualiza o restante do corpo (cada parte assumindo a antiga posição da cabeça)
		for posicao in self.posicoes[1:]:
			posicao_atual = posicao.copy()
			posicao["x"] = antiga_cabeca["x"]
			posicao["y"] = antiga_cabeca["y"]
			posicao["direcao_antiga"] = antiga_cabeca["direcao_antiga"]
			posicao["direcao_nova"] = antiga_cabeca["direcao_nova"]
			antiga_cabeca = posicao_atual

		# Desenha cada parte do corpo
		for num_pos, posicao_nova in enumerate(self.posicoes):
			posicao_x = posicao_nova["x"]
			posicao_y = posicao_nova["y"]
			direcao_antiga = posicao_nova["direcao_antiga"]
			direcao_nova = posicao_nova["direcao_nova"]

			print("*"  if direcao_antiga != direcao_nova else "#", end="")

			if num_pos == 0: # Gerencia a parte da Cabeca
				cor = self.cor_cabeca
				# Roda o Sprite da Cabeça conforme a Direção que a cobrinha está
				imagem = pygame.transform.rotate(self.imagens_transformadas["cabeca"], self.direcoes_cabeca_rabo[direcao_nova])
			elif num_pos == len(self.posicoes)-1: # Gerencia a parte do Rabo
				cor = self.cor_rabo
				# Roda o Sprite do Rabo conforme a Direção que a cobrinha está
				if direcao_nova != direcao_antiga: # Checa a dobra esta próxima do rabo, preparando ele para dobrar
					direcao_do_rabo = direcao_nova
				else:
					direcao_do_rabo = direcao_antiga
				# direcao_do_rabo = direcao_antiga if posicao_x != posicao_y else direcao_nova
				imagem = pygame.transform.rotate(self.imagens_transformadas["rabo"], self.direcoes_cabeca_rabo[direcao_do_rabo])
			else: # Gerencia o restante do Corpo
				cor = self.cor
				if direcao_antiga == direcao_nova: # Checa se está parte do corpo esta na mesma direção
					if direcao_antiga in ["esquerda", "direita"]: # Se está indo para a Direita ou Esquerda, tronco na Horizontal
						imagem = self.imagens_transformadas["tronco"]
					else:
						imagem = pygame.transform.rotate(self.imagens_transformadas["tronco"], 90) # Se está indo para Cima ou Para Baixo, tronco rotacionado em 90 graus
				else: # Se as direções Nova e Antiga forem diferentes, ocorrerá uma dobra
					# Possivéis dobradas:
					# Baixo    > Direita; Baixo    > Esquerda;
					# Cima     > Direita; Cima     > Esquerda;
					# Direita  > Baixo;   Direita  > Cima;
					# Esquerda > Baixo;   Esquerda > Cima.
					if (direcao_antiga == "direita" and direcao_nova == "cima") or (direcao_antiga == "baixo" and direcao_nova == "esquerda"):
						imagem = self.imagens_transformadas["dobrada"]
					elif (direcao_antiga == "direita" and direcao_nova == "baixo") or (direcao_antiga == "cima" and direcao_nova == "esquerda"):
						imagem = self.imagens_transformadas["dobrada_2"]
					elif (direcao_antiga == "esquerda" and direcao_nova == "baixo") or (direcao_antiga == "cima" and direcao_nova == "direita"):
						imagem = pygame.transform.rotate(self.imagens_transformadas["dobrada"], 180)
					else:
						imagem = pygame.transform.rotate(self.imagens_transformadas["dobrada_2"], 180)

			if self.exibicao: # Mostra ou Não a área de contato da Cobra
				pygame.draw.rect(surface, self.cor, (posicao_x, posicao_y, self.tamanho-1, self.tamanho-1))

			# Desenha o Sprite Selecionado
			surface.blit(imagem, (posicao_x, posicao_y))
		print()
		# Após Atualizar e Desenhar todas as partes, o corpo entrará na mesma direção
		self.posicoes[0]["direcao_antiga"] = self.posicoes[0]["direcao_nova"]

		# Verifica se a Cabeça acertou alguma parte do Corpo (morte)
		if self.posicoes[0] in self.posicoes[1:]:
			self.estado = False

		
	def para_esquerda(self):
		# Define a direção antiga
		self.direcao_antiga = self.direcao
		# Evita que a cobrinha volte para "trás"
		self.direcao = "esquerda" if self.direcao != "direita" else "direita"
		if self.direcao != self.direcao_antiga: # Checa se a direção será alterada
			# Atribui as direções à variável da cobrinha
			self.posicoes[0]["direcao_antiga"] = self.direcao_antiga
			self.posicoes[0]["direcao_nova"] = self.direcao
	

	def para_direita(self):
		self.direcao_antiga = self.direcao
		self.direcao = "direita" if self.direcao != "esquerda" else "esquerda"
		if self.direcao != self.direcao_antiga:
			self.posicoes[0]["direcao_antiga"] = self.direcao_antiga
			self.posicoes[0]["direcao_nova"] = self.direcao
	

	def para_cima(self):
		self.direcao_antiga = self.direcao
		self.direcao = "cima" if self.direcao != "baixo" else "baixo"
		if self.direcao != self.direcao_antiga:
			self.posicoes[0]["direcao_antiga"] = self.direcao_antiga
			self.posicoes[0]["direcao_nova"] = self.direcao
	

	def para_baixo(self):
		self.direcao_antiga = self.direcao
		self.direcao = "baixo" if self.direcao != "cima" else "cima"
		if self.direcao != self.direcao_antiga:
			self.posicoes[0]["direcao_antiga"] = self.direcao_antiga
			self.posicoes[0]["direcao_nova"] = self.direcao

	def get_infos(self, surface):
		system("cls")

		for n_parte, parte in enumerate(self.posicoes):
			pos_x = parte["x"]
			pos_y = parte["y"]
			direcao_antiga = parte["direcao_antiga"]
			direcao_nova = parte["direcao_nova"]

			# print(f"Parte: {n_parte}\nx: {pos_x}\ny: {pos_y}\nAntiga: {direcao_antiga}\nNova: {direcao_nova}\n")
		print(90)
		surface.blit(pygame.transform.rotate(self.imagens_transformadas["dobrada"], 90), (100, 100))
		print(180)
		surface.blit(pygame.transform.rotate(self.imagens_transformadas["dobrada"], 180), (100, 150))
		print(270)
		surface.blit(pygame.transform.rotate(self.imagens_transformadas["dobrada"], 270), (100, 200))
		print(360)
		surface.blit(pygame.transform.rotate(self.imagens_transformadas["dobrada"], 360), (100, 250))

