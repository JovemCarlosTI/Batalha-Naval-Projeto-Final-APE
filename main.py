# Alessandro, Alex, Bruno, Caio e Carlos 

import random as rd

# Variáveis Globais
matriz_Q = 8 # Ordem da matriz
msg_pos_tabuleiro = ''
jogadaDaVez = 1
contRodada = 0
qtdNaviosJ1, qtdNaviosJ2 = 0, 0
qtdNavios = 0
t1, t2 = [], []
nome_arq_save = ''

#função p/ criação de tabuleiros.
def gerarTabuleiros(qtdNavios):
	while True:
		global matriz_Q

		# Vetor com onda e N, para sorteio
		char = ['\033[36m≋\033[0m', '\033[1mN\033[0m']
		t = [[char[0]] * matriz_Q for i in range(matriz_Q)]

		qtdNaviosRestantes = qtdNavios
		for i in range(matriz_Q):
			for j in range(matriz_Q):
				if qtdNaviosRestantes > 0:
					# Escolhe entre onda e navio (onda com peso de 5/6 e navio 1/6)
					escolha = rd.choices(char, weights=(0.906, 0.094))[0]
					t[i][j] = escolha
					# Se foi um navio escolhido
					if escolha == '\033[1mN\033[0m':
						qtdNaviosRestantes -= 1
				else:
					break
		
		valido = verificarTabuleiro(t)
    # Se for um tabuleiro válido
		if qtdNaviosRestantes == 0 and valido:
			break
			
	return t


# Função para verificar existência de navios adjacentes entre si
def verificarTabuleiro(tabuleiro):
  for linha in range(len(tabuleiro)):
		# Se tem um navio na linha
    if tabuleiro[linha].count('\033[1mN\033[0m'):
			# Checar a partir do primeiro navio até o fim da linha
      for coluna in range(tabuleiro[linha].index('\033[1mN\033[0m'), matriz_Q):
        if tabuleiro[linha][coluna] == '\033[1mN\033[0m':

          antecessorLinha, sucessorLinha = linha - 1, linha + 1
          antecessorColuna, sucessorColuna = coluna - 1, coluna + 1

          if not (antecessorColuna < 0):
            # Verifica bloco esquerdo
            if tabuleiro[linha][antecessorColuna] == '\033[1mN\033[0m':
              return False
            if not (antecessorLinha < 0):
              # Verifica diagonal esquerda superior
              if tabuleiro[antecessorLinha][antecessorColuna] == '\033[1mN\033[0m':
                return False
            if not (sucessorLinha >= matriz_Q):
              # Verifica diagonal esquerda inferior
              if tabuleiro[sucessorLinha][antecessorColuna] == '\033[1mN\033[0m':
                return False

          if not (sucessorColuna >= matriz_Q):
            # Verifica bloco direito
            if tabuleiro[linha][sucessorColuna] == '\033[1mN\033[0m':
              return False
            if not (antecessorLinha < 0):
              # Verifica diagonal direita superior
              if tabuleiro[antecessorLinha][sucessorColuna] == '\033[1mN\033[0m':
                return False
            if not (sucessorLinha >= matriz_Q):
              # Verifica diagonal direita inferior
              if tabuleiro[sucessorLinha][sucessorColuna] == '\033[1mN\033[0m':
                return False

          if not (antecessorLinha < 0):
            # Verifica bloco acima
            if tabuleiro[antecessorLinha][coluna] == '\033[1mN\033[0m':
              return False
          if not (sucessorLinha >= matriz_Q):
            # Verifica bloco abaixo
            if tabuleiro[sucessorLinha][coluna] == '\033[1mN\033[0m':
              return False

  return True


#função auxiliar p/ converter matriz em texto.
def matriz_to_string(matriz):
  matriz_em_string = ''
  for linha in matriz:
    for e in linha:
      matriz_em_string += e + ','
			# Tirando o separador desnecessário no final
    matriz_em_string = matriz_em_string[0:-1]
    matriz_em_string += ';'
			# Tirando o separador desnecessário no final
  matriz_em_string = matriz_em_string[0:-1]

  return matriz_em_string


#função auxiliar p/ converter texto de matriz em matriz.
def string_to_matriz(matriz_em_string):
  matriz_em_string = matriz_em_string.replace('\n', '')
  return [linha.split(',') for linha in matriz_em_string.split(';')]


#funçao p/ salvar o jogo.
def salvar_jogo():
  global nome_arq_save, t1, t2, contRodada, jogadaDaVez, qtdNavios, qtdNaviosJ1, qtdNaviosJ2
  with open(nome_arq_save, "w") as arquivo:
    arquivo.write(matriz_to_string(t1) + "\n")
    arquivo.write(matriz_to_string(t2) + "\n")
    arquivo.write(str(contRodada) + "\n")
    arquivo.write(str(jogadaDaVez) + "\n")
    arquivo.write(str(qtdNavios) + "\n")
    arquivo.write(str(qtdNaviosJ1) + "\n")
    arquivo.write(str(qtdNaviosJ2) + "\n")


#função p/ carregar o jogo.
def carregar_jogo():
  global nome_arq_save, t1, t2, contRodada, jogadaDaVez, qtdNavios, qtdNaviosJ1, qtdNaviosJ2
  with open(nome_arq_save, 'r') as arquivo:
    t1 = string_to_matriz(arquivo.readline())
    t2 = string_to_matriz(arquivo.readline())
    contRodada = int(arquivo.readline().replace('\n', ''))
    jogadaDaVez = int(arquivo.readline().replace('\n', ''))
    qtdNavios = int(arquivo.readline().replace('\n', ''))
    qtdNaviosJ1 = int(arquivo.readline().replace('\n', ''))
    qtdNaviosJ2 = int(arquivo.readline().replace('\n', ''))


#função p/ mostrar o(s) tabuleiro(s).
def imprimeTabuleiro(t1, t2, exibirNavios=False):
	global jogadaDaVez, msg_pos_tabuleiro
	
	# Cabeçalho de jogadores
	j1, j2 = "Jogador 1", "Jogador 2"
	if jogadaDaVez == 1:
		j1 = '🔫 ' + j1
		j2 = '🎯 ' + j2
	else:
		j2 = '🔫 ' + j2
		j1 = '🎯 ' + j1
		
	print('\n' * 10)  # Limpa a tela anterior pro novo tabuleiro
	
		# Configurações padrões repetidas
	margem_inical, margem_tabuleiros = ' ' * 2, ' ' * 8
	div_linha = margem_inical * 2 + '\033[30m+\033[0m' + ('\033[30m-\033[0m' * 3 + '\033[30m+\033[0m') * 8 + margem_tabuleiros + margem_inical + "\033[30m +\033[0m" + ('\033[30m-\033[0m' * 3 + '\033[30m+\033[0m') * 8
	div_coluna = '\033[30m | \033[0m'

  # Jogador 1  Jogador 2
	print(
		f'{j1:^42}{j2:^43}\n')
	posicoes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

  # Cabeçalho de colunas
	cabecalho = ''.join([''.join(e + div_coluna) for e in posicoes])
	print(
    f'{margem_inical*3}{cabecalho}{margem_tabuleiros}{margem_inical*2}{cabecalho}'
  )

  # Linha a linha
	for i in range(matriz_Q):
		print(div_linha)
		linha1 = ''.join([
      ''.join(('\033[36m≋\033[0m' if e == '\033[1mN\033[0m' and not exibirNavios else e) + div_coluna)
      for e in t1[i]
    ])
		linha2 = ''.join([
      ''.join(('\033[36m≋\033[0m' if e == '\033[1mN\033[0m' and not exibirNavios else e) + div_coluna)
      for e in t2[i]
    ])
		print(
      f'{margem_inical}{posicoes[i]}{div_coluna}{linha1}{margem_tabuleiros}{posicoes[i]}{div_coluna}{linha2}'
    )
	print(div_linha)
	print(msg_pos_tabuleiro)
	msg_pos_tabuleiro = ''


#função p/ carregar cada rodada
def carregarRodada(jogadaDaVez, jogoCarregado=False):
  global contRodada, msg_pos_tabuleiro
  print(f"\033[1mRodada nº {contRodada + 1}\033[0m")

  # Pergunta se salva o jogo
  # Só pergunta se não acabou de carregar (to-do)
  if not jogoCarregado:
    entrada = input("""\n\033[1mDeseja salvar o jogo?\033[0m
		Y - Sim
		Qualquer valor - Não
		""").upper() 
    if entrada == 'Y':
      print("💾 \033[3mSalvando jogo, aguarde...\033[0m")
      salvar_jogo()
  # Pergunta se exibe os navios
  entrada = input("""\n\033[1mDeseja ver os navios?\033[0m
	 	Y - Sim
	 	Qualquer valor - Não
	   """).upper()
  if entrada == 'Y':
    exibirNavios = True
  else:
    exibirNavios = False

  # Exibir tabuleiros
  imprimeTabuleiro(t1, t2, exibirNavios)
  print(f"\033[1mRodada nº {contRodada + 1}\033[0m")

  x, y = 0, 0
  coordenadas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
  while not (x in coordenadas) or not (y in coordenadas):  # Enquanto x e y não forem coordenadas válidas!
    print(f"Jogador {jogadaDaVez}, informe as coordenadas do seu disparo!")

    y = input("- Linha (A a H): ").upper()
    if y not in coordenadas:
      imprimeTabuleiro(t1, t2, exibirNavios)
      print("\033[31m❌ Linha inexistente! Informe uma linha válida\033[0m\n")
      continue

    x = input("- Coluna (A a H): ").upper()
    if x not in coordenadas:
      imprimeTabuleiro(t1, t2, exibirNavios)
      print("\033[31m❌ Coluna inexistente! Informe uma linha válida\033[0m\n")
      continue

  if jogadaDaVez == 1:
    jogadorAlvo = 2
  elif jogadaDaVez == 2:
    jogadorAlvo = 1

  # Converte A-H para 0-7
  x, y = coordenadas.index(x), coordenadas.index(y)

  realizarDisparo(jogadorAlvo, x, y)
  contRodada += 1
  imprimeTabuleiro(t1, t2, exibirNavios)


#Realização do Disparo
def realizarDisparo(jogadorAlvo, x, y):
  global msg_pos_tabuleiro, qtdNaviosJ1, qtdNaviosJ2, jogadaDaVez, contRodada
	# Variáveis de fogo e água
  fogo, agua = '\033[31m\033[1mF\033[0m', '\033[96m\033[1mA\033[0m'

	# Variáveis de mensagens
  msg_fogo, msg_agua, msg_disparo_feito = '\033[31m💥 FOGO\033[0m', '\033[96m🌊 ÁGUA\033[0m', '\033[95mDisparo já realizado nessa posição\033[0m'
	
  if jogadorAlvo == 1:
    tabuleiroAlvo = t1
  else:
    tabuleiroAlvo = t2

	# Se acertou um navio
  if tabuleiroAlvo[y][x] == '\033[1mN\033[0m':
		# Fogo
    tabuleiroAlvo[y][x] = fogo
    msg_pos_tabuleiro = msg_fogo
    if jogadorAlvo == 1:
      qtdNaviosJ1 -= 1
    else:
      qtdNaviosJ2 -= 1
			
	# Se já atirou nesse lugar
  elif tabuleiroAlvo[y][x] == agua or tabuleiroAlvo[y][x] == fogo:
	  # Não pode
	  msg_pos_tabuleiro = msg_disparo_feito
	  contRodada -= 1
		
	# Se errou o tiro
  else:
    # Água
    msg_pos_tabuleiro = msg_agua
    tabuleiroAlvo[y][x] = agua
    if jogadaDaVez == 1:
      jogadaDaVez = 2
    else:
      jogadaDaVez = 1
  print()
# Iniciar o jogo
def iniciar_jogo():
  global t1, t2, qtdNaviosJ1, qtdNaviosJ2, qtdNavios
  while True:
    qtdNavios = input("\033[1mQuantidade de navios da partida (1 a 6): \033[0m")
    if not qtdNavios.isnumeric() or int(qtdNavios) < 1 or int(qtdNavios) > 6:
        print("Quantidade de navios inválida!")
    else:
        qtdNavios = int(qtdNavios)
        break
			
  print('Gerando tabuleiro do jogador 1...')
  t1 = gerarTabuleiros(qtdNavios)
  qtdNaviosJ1 = qtdNavios
  print('Gerando tabuleiro do jogador 2...')
  t2 = gerarTabuleiros(qtdNavios)
  qtdNaviosJ2 = qtdNavios


# PROGRAMA PRINCIPAL
# Inicio do jogo
cabecalho = '\033[0m\033[1m  \033[21mBatalha Naval\033[0m  \033[36m'
print(f'\033[36m{cabecalho:≋^68}\033[0m\n')
print()

# Pergunta se deseja criar um save
entrada = input("""\n\033[1mDeseja criar um arquivo de save para essa partida?\033[0m
	Y - Sim
	Qualquer Valor - Não
	 """).upper()
print()
if entrada == 'Y':
  # Solicita nome de arquivo save e cria
  nome_arq_save = input("\033[1mInforme um nome para o seu arquivo de save: \033[0m")
  arq = open(nome_arq_save, 'w')
  arq.close()
  iniciar_jogo()
else:
  # Pergunta se já tem arquivo de save anterior
	entrada = input("""\n\033[1mDeseja carregar um jogo anterior?\033[0m
	Y - Sim
	Qualquer Valor - Não
	 """).upper()
	if entrada == 'Y':
			nome_arq_save = input("\033[1mInforme um nome para o seu arquivo de save: \033[0m")
		# Para evitar erro de I/O com o read
			arquivo = open(nome_arq_save, 'a')
			arquivo.close()
			with open(nome_arq_save, "r") as arquivo:
				# Se o arquivo não está vazio 
				if (arquivo.read() != ''):
						print('Carregando...')
						carregar_jogo()
						# Começar rodada com jogo carregado
						carregarRodada(jogadaDaVez, True)
				else:
					# Se está vazio, começar jogo do zero com nome do arquivo informado
						print(f'Arquivo inexistente ou vazio, gerando um arquivo de save chamado {nome_arq_save}...')
						iniciar_jogo()
	else:
		# Começar jogo do zero
		iniciar_jogo()
		nome_arq_save = 'save.txt'

imprimeTabuleiro(t1, t2)

while qtdNaviosJ1 > 0 and qtdNaviosJ2 > 0:
  carregarRodada(jogadaDaVez)

# Final do jogo
print()
print(f"\033[32m 🎉Parabéns, jogador {jogadaDaVez}! Você venceu o jogo! 🎉\033[0m")
print()
if jogadaDaVez == 1:
  print(f"\033[32m Jogador(a) 2: {qtdNavios - qtdNaviosJ1} / {qtdNavios}\033[0m")
else:
  print(f"\033[32m Jogador(a) 1: {qtdNavios - qtdNaviosJ2} / {qtdNavios}\033[0m")