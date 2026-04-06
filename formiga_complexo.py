##############################################
#         INTELIGÊNCIA ARTIFICIAL    		 #
# Tarefa 1 - Organização de Formigas Parte 2 #
# ALUNOS: Caio Marquiafave Carregari         #
#		  Clidenor Barbosa de Melo Neto      # 
##############################################

#############################################
#         Lista de símbolos usados          #
#  'X' -> Formiga viva                      #
#  '1'...'15' -> São dados                  #
#  '@' -> Formiga viva carregando corpo     #
#  '#' -> Representa a borda da matriz      #
#############################################

# Bibliotecas importadas
import random
import math
import numpy as np

# Configurações
TAMANHO_MATRIZ = 80
QTD_FORMIGAS = 125
QTD_CORPOS = 600
QTD_GRUPOS = 15
RAIO = 1
DESVIO_PADRAO = 2
MEDIA = 15
MAX_ITERACOES = 20000000

# Classe formiga para manter o controle
class Formiga:
    def __init__(self, pos):
        self.pos = pos
        self.carregando = False 
        self.dado = None
        
# Classe de dados para manter o controle
class Dados:
    def __init__(self, pos, valores, peso):
        self.pos = pos
        self.valores = valores
        self.peso = peso

# Função para montar a matriz
def montarMatriz(tamanho): 
    matrix = [[' ' for _ in range(tamanho + 2)] for _ in range(tamanho + 2)]
    
    for i in range (tamanho + 2):
        for j in range (tamanho + 2):
            if(i == 0 or i == (tamanho + 1) or j == 0 or j == (tamanho + 1 )):
                matrix[i][j] = '#'
    
    return matrix

# Função para mostrar a matriz
def mostrarMatriz(matrix):
    for linha in matrix:
        print(' '.join(map(str, linha)))

# Função que conecta as bordas da matriz (movimento toroidal)
def moverBordas(pos, dx, dy):
    x, y = pos
    nx = ((x + dx - 1) % TAMANHO_MATRIZ) + 1
    ny = ((y + dy - 1) % TAMANHO_MATRIZ) + 1
    return (nx, ny)

# Função para checar se a posição de movimento é válida
def posicaoValida(matrix, pos):
    dx, dy = pos
    
    if (1 <= dx <= TAMANHO_MATRIZ and 1 <= dy <= TAMANHO_MATRIZ):
        return True
    
    return False

# Função para checar se na posição existe um corpo morto
def posicaoItem(matrix, pos):
    dx, dy = pos
    
    if (matrix[dx][dy].isdigit()):
        return True
    
    return False

# Função para checar se na posição existe uma formiga
def posicaoFormiga(matrix, pos):
    dx, dy = pos
    
    if (matrix[dx][dy] == 'X' or matrix[dx][dy] == '@'):
        return True
    else:
        return False

# Função para checar os itens vizinhos 
def checarItensVizinhos(matrix, pos, dictCorpos, raio=RAIO):
    fx, fy = pos
    itensVizinhos = list()
    
    for dx in range(-raio, raio + 1):
        for dy in range(-raio, raio + 1):
            if dx == dy == 0:
                continue 
            
            nx, ny = fx + dx, fy + dy
            if (1 <= nx <= TAMANHO_MATRIZ and 1 <= ny <= TAMANHO_MATRIZ):
                if (posicaoItem(matrix, (nx, ny))):
                    dado_vizinho = dictCorpos.get((nx, ny))
                    if (dado_vizinho):
                        itensVizinhos.append(dado_vizinho)
    
    return itensVizinhos

# Função para calcular a distância euclidiana
def distanciaEuclidiana(dado, vizinhos):
    distancias = []
    for v in vizinhos:
        dx = dado.valores[0] - v.valores[0]
        dy = dado.valores[1] - v.valores[1]
        dz = abs((dado.peso - v.peso)  * 100) # Manter o controle pelo peso. Se peso for igual, anula. Se peso for diferente, diminui as chances de largar
        distancias.append(math.sqrt(dx**2 + dy**2 + dz**2))
    return distancias

# Função para calcular a similaridade
def similaridade(matrix, dado, pos, dictCorpos, raio_base=RAIO, max_expande=3):
    alpha = 67.0
    raio_eff = raio_base
    tentativa = 0
    vizinhos = checarItensVizinhos(matrix, pos, dictCorpos, raio=raio_eff)
    s = len(vizinhos)

    if (s == 0):
        return 0.0
    
    while s <= 3 and tentativa < max_expande:
        tentativa += 1
        raio_eff += 1
        vizinhos = checarItensVizinhos(matrix, pos, dictCorpos, raio=raio_eff)
        s = len(vizinhos)

    distancias = distanciaEuclidiana(dado, vizinhos)

    funcao = 0.0
    for dist in distancias:
        funcao += 1.0 - (dist / alpha)

    resultado = (funcao / s)
    return max(0.0, min(1.0, resultado))

# Função para formiga pegar o item
def pegarItem(matrix, dado, dictCorpos):    
    k1 = 0.01

    if (dado):
        f = similaridade(matrix, dado, dado.pos, dictCorpos, raio_base=RAIO, max_expande=3)

        Pp = float((k1 / (k1 + f))**2)
    
        if (random.random() < Pp):
         return True
    
        return False
    
    return False
    
# Função para formiga largar o item
def largarItem(matrix, dado, dictCorpos):
    k2 = 0.001
    
    if (dado):
        f = similaridade(matrix, dado, dado.pos, dictCorpos, raio_base=RAIO, max_expande=3)
        
        Pd = float((f / (k2 + f))**2)
        
        if (random.random() < Pd):
            return True
        
        return False
    return False
        
# Função para inserir formigas e corpos
def inserirFormigasCorpos(matrix, listaFormigas, dictCorpos):
    #medias = [(MEDIA, MEDIA), (MEDIA, -MEDIA), (-MEDIA, MEDIA), (-MEDIA, -MEDIA)]
    medias = [(MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA), 
              (MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA), (MEDIA, MEDIA)]
    while len(listaFormigas) != QTD_FORMIGAS:
        pos = tuple(random.randint(1, TAMANHO_MATRIZ) for _ in range (2))
        
        if (posicaoValida(matrix, pos) and not posicaoItem(matrix, pos)):
            dx, dy = pos
            matrix[dx][dy] = 'X'
            nova_formiga = Formiga(pos)
            listaFormigas.append(nova_formiga)

    for peso, (mx, my) in enumerate(medias, start=1):
        inseridos = 0
        while inseridos < QTD_CORPOS // QTD_GRUPOS:
            pos = tuple(random.randint(1, TAMANHO_MATRIZ) for _ in range(2))
            if (posicaoValida(matrix, pos) and not posicaoFormiga(matrix, pos) and pos not in dictCorpos):
                dx, dy = pos
                matrix[dx][dy] = str(peso)
                
                vx = float(np.random.normal(loc=mx, scale=DESVIO_PADRAO))
                vy = float(np.random.normal(loc=my, scale=DESVIO_PADRAO))
                
                valor = (vx, vy)
                dictCorpos[pos] = Dados(pos, valor, peso)
                inseridos += 1

# Gera a matriz atual do checkpoint
def gerarMatrizAtual(listaFormigas, dictCorpos):
    matriz = [[' ' for _ in range(TAMANHO_MATRIZ + 2)] for _ in range(TAMANHO_MATRIZ + 2)]

    # bordas
    for i in range(TAMANHO_MATRIZ + 2):
        matriz[0][i] = matriz[TAMANHO_MATRIZ + 1][i] = '#'
        matriz[i][0] = matriz[i][TAMANHO_MATRIZ + 1] = '#'

    # corpos
    for dado in dictCorpos.values():
        x, y = dado.pos
        matriz[x][y] = str(dado.peso)

    # formigas
    for formiga in listaFormigas:
        x, y = formiga.pos
        
        if(formiga.carregando):
            matriz[x][y] = '@' 
        else:
            matriz[x][y] = 'X'

    return matriz

# Função para movimentar as formigas
def movimentarFormigas(matrix, listaFormigas, dictCorpos):
    for formiga in listaFormigas:
        fx, fy = formiga.pos
        
        # A formiga escolhe uma direção e calcula a nova posição
        dx, dy = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
        nova_pos = moverBordas((fx, fy), dx, dy)

        # Possibilidade da formiga largar o corpo se estiver carregando
        if (formiga.carregando):
            
            formiga.dado.pos = nova_pos
            formiga.pos = nova_pos
            if (not dictCorpos.get(nova_pos) and largarItem(matrix, formiga.dado, dictCorpos) and not posicaoFormiga(matrix, nova_pos)):
                formiga.carregando = False
                formiga.dado.pos = formiga.pos
                dictCorpos[formiga.dado.pos] = formiga.dado
                formiga.dado = None

        # Possibilidade da formiga pegar um corpo
        else:
            
            # A formiga está em cima de um corpo
            dado = dictCorpos.get(nova_pos)
            if (dado and pegarItem(matrix, dado, dictCorpos)):
                formiga.pos = nova_pos
                formiga.carregando = True
                formiga.dado = dado
                dictCorpos.pop(dado.pos, None)

            # A formiga não está em cima de um corpo e apenas se move
            else:
                formiga.pos = nova_pos
    
# Função main para rodar o código
def main():
    listaFormigas = []
    dictCorpos = {}
    matriz_logs = []  # snapshots (iteracao, matriz)
    matriz = montarMatriz(TAMANHO_MATRIZ)
    inserirFormigasCorpos(matriz, listaFormigas, dictCorpos)

    # definindo checkpoints
    meio = MAX_ITERACOES // 2
    checkpoints = {1, meio}  # 1ª e meio 

    for iteracao in range(1, MAX_ITERACOES + 1):

        matriz_atualizada_para_logica = gerarMatrizAtual(listaFormigas, dictCorpos)
        movimentarFormigas(matriz_atualizada_para_logica, listaFormigas, dictCorpos)

        # captura apenas nos checkpoints
        #if iteracao in checkpoints:
        if (iteracao % 500000 == 0 or iteracao == 1):
            matriz_atual = gerarMatrizAtual(listaFormigas, dictCorpos)
            matriz_logs.append((iteracao, matriz_atual))
            print(f"\nIteração: {iteracao}\n"
                  f"Formigas: {len(listaFormigas)}\n"
                  f"Tamanho Matriz: {TAMANHO_MATRIZ}\n"
                  f"Dados: {len(dictCorpos)}\n"
                  f"Raio: {RAIO}")
            mostrarMatriz(matriz_atual)

    for formiga in listaFormigas:
        if (formiga.carregando):
            x, y = formiga.pos
            dx, dy = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
            nova_pos = moverBordas((x, y), dx, dy)
            
            dictCorpos[formiga.pos] = formiga.dado
            formiga.carregando = False
            formiga.dado = None
            formiga.pos = nova_pos
                  
    matriz_final = gerarMatrizAtual(listaFormigas, dictCorpos)
    matriz_logs.append((MAX_ITERACOES, matriz_final))
    print(f"\nIteração FINAL: {MAX_ITERACOES}\n"
          f"Formigas: {len(listaFormigas)}\n"
          f"Tamanho Matriz: {TAMANHO_MATRIZ}\n"
          f"Dados: {len(dictCorpos)}\n"
          f"Raio: {RAIO}")
    mostrarMatriz(matriz_final)

if __name__ == "__main__":
	main()
 
 
# Iteração: 20000000
# Formigas: 125
# Tamanho Matriz: 50
# Dados: 400
# Raio: 1
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                     4 4 4     X     X     X               X X       #
#                                                 4 4 4 4 4 4 X                                       #
#       X     X                       X         4 4 4 4   4 4 4 4     X                               #
#                                               4 4 4 4 4 4 4 4 4                                   X #
#                                   X       4 4 X   4 4   4 4 4           X             X             #
#     X                   X                 4 4 4 4 4 4   4   4 4             X                       #
#     X                                     4   4 4   4 4 4 4   4                                     #
#                                         4 4 4 4 4 4 4 4 4 X 4 4 X                                   #
#                                         4 4   4 4 4 4   X 4 4 4                                     #
#                                             4 4   4 4 4 4 4 4 4                     X               #
#         X                                     4 4 4 4 4 4 4 4                   X X             X   #
#                                                 4 4 4 4 4 4                   X                     #
#       X         X                                 X   X 4 X       X                                 #
#   X             X                                   X   4 4                 2 2 2             X     #
#                                                           X       X         X 2 X 2                 #
#               X                                                         2 2 2 2 2 2 2 2 2 2 2       #
#                           X   X                                         2 2 2 2 2 2 2 2 2 2 2       #
#     X               X       X           X     X       X               X   2 2 2 2 2 2 2 2 2 2 2 2   #
#                                       X                 X                 2 2 2 2 2 2 2   2 2   2 2 #
#         3   3   X                               X                         2 2 2 2 X 2 2 2 2 2 2 2 2 #
#         3 3 3 3                                                         2 2   2 2 2   2 2 X 2 2 X X #
#         3 3 3 3 3             3 3 3               X                     2 2 X   2 2 2 2 2 2 2       #
#         3 3 3   3 3 3 3 3   3 3 3 3                               X     2 2 X     X     2 2 2       #
#         3 3 3 3 3 3 3 3 3 3 3 3 X                                         2 2         2 2 2 2       #
#       X   3 3 3   3 3 3 3 3 3 3             X                                             2         #
#           3 3 3 3 3 3   3   3                           X                                           #
#       3 3 X   3 3 3 3 3 X 3                                           X                             #
#         3 3 3 3 3   3 3 3 3                                                                         #
# X       3 3 3   3 3 3 3 3 3 X                                                                       #
#           3 3 3 3 3 3 3                                 X                                   X       #
#             3 3 3 3 3 3                 X                                                           #
#           X     3 3                 X                 X                                   X         #
#     X                                             X                                                 #
#           X                   X                             X             X                         #
#   X                                   X           X X     X                             X           #
#                         X                                                                           #
#                                       1 1                                                       X   #
#                                   1 1 1 1     X X       X X                                         #
#                                 1 1   1 1 1 1 1                     X                     X         #
#                               1 1 1 1 1 1 1 1 1 1                                   X               #
#                               1 X   1 1 1 1 1   X 1               X           X                     #
#                           X 1 1   1 1 1     1 1 1 1 1 X 1                                           #
#           X                 1 1 1 1   1 1 1 1 1 1 1 1 1 1                   X                       #
#   X                       1 1 1 1 1 1   1   1   1     1 1                                           #
#                           1 1 1   1 1 1 1 1 1 1 1 1 1 1       X                       X             #
#     X                     1 1 1 1   1 1 1 1 1 1   1 1 1                                             #
#           X                   1 X 1 1   X                             X                             #
#                                                     X                                               #
#                                                   X                                           X     #
#   X                                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #