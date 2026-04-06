##############################################
#         INTELIGÊNCIA ARTIFICIAL    		 #
# Tarefa 1 - Organização de Formigas Parte 1 #
# ALUNOS: Caio Marquiafave Carregari         #
#		  Clidenor Barbosa de Melo Neto      # 
##############################################

#############################################
#         Lista de símbolos usados          #
#  'o' -> Corpo morto de uma formiga        #
#  'X' -> Formiga viva                      #
#  '@' -> Formiga viva carregando corpo     #
#  '#' -> Representa a borda da matriz      #
#############################################

# Bibliotecas importadas
import random
import time

# Configurações
TAMANHO_MATRIZ = 25
QTD_FORMIGAS = 10
QTD_CORPOS = 150
RAIO = 1

# Classe formiga para manter o controle
class Formiga:
    def __init__(self, pos):
        self.pos = pos
        self.carregando = False 

# Função para montar a matriz
def montar_matriz(tamanho): 
    matrix = [[' ' for _ in range(tamanho + 2)] for _ in range(tamanho + 2)]
    
    for i in range (tamanho + 2):
        for j in range (tamanho + 2):
            if(i == 0 or i == (tamanho + 1) or j == 0 or j == (tamanho + 1 )):
                matrix[i][j] = '#'
    
    return matrix

# Função para mostrar a matriz
def mostrar_matriz(matrix):
    for linha in matrix:
        print(' '.join(map(str, linha)))

# Função para checar se a posição de movimento é válida
def posicao_valida(matrix, pos):
    dx, dy = pos
    
    if (1 <= dx <= TAMANHO_MATRIZ and 1 <= dy <= TAMANHO_MATRIZ):
        return True
    
    return False

# Função para checar se na posição existe um corpo morto
def posicao_item(matrix, pos):
    dx, dy = pos
    
    if (matrix[dx][dy] == 'o'):
        return True
    else:
        return False

# Função para checar se na posição existe uma formiga
def posicao_formiga(matrix, pos):
    dx, dy = pos
    
    if (matrix[dx][dy] == 'X'):
        return True
    else:
        return False

# Função para checar os itens vizinhos 
def checar_itens_vizinhos(matrix, pos):
    fx, fy = pos
    itens_vizinho = 0
    
    for dx in range(-RAIO, RAIO + 1):
        for dy in range(-RAIO, RAIO + 1):
            if dx == 0 and dy == 0:
                continue 
            
            nx, ny = fx + dx, fy + dy
            if (1 <= nx <= TAMANHO_MATRIZ and 1 <= ny <= TAMANHO_MATRIZ):
                if (posicao_item(matrix, (nx, ny))):
                    itens_vizinho += 1
    
    return itens_vizinho

# Função para formiga pegar o item
def pegar_item(matrix, pos, visao):    
    if (posicao_item(matrix, pos)):
        
        itens_vizinhos = checar_itens_vizinhos(matrix, pos)
        probabilidade_pegar = 1 - (itens_vizinhos / visao)
        
        if (probabilidade_pegar > 0.5):
            return True
        elif (probabilidade_pegar < 0.5):
            return False
        else:
            return random.choice([True, False])

# Função para formiga largar o item
def largar_item(matrix, pos, visao):
    if (posicao_valida(matrix, pos)):
        
        itens_vizinhos = checar_itens_vizinhos(matrix, pos)
        probabilidade_largar = itens_vizinhos / visao
        
        if (probabilidade_largar > 0.5):
            return True
        elif (probabilidade_largar < 0.5):
            return False
        else:
            return random.choice([True, False])
        
# Função para inserir as formigas e os corpos na matriz   
def inserir_formigas_corpos(matrix, listaFormigas, setCorpos):
    
    while len(listaFormigas) != QTD_FORMIGAS:
        pos = tuple(random.randint(1, TAMANHO_MATRIZ) for _ in range (2))
        
        if (posicao_valida(matrix, pos) and not posicao_item(matrix, pos)):
            dx, dy = pos
            matrix[dx][dy] = 'X'
            nova_formiga = Formiga(pos)
            listaFormigas.append(nova_formiga)

    while len(setCorpos) != QTD_CORPOS:
        pos = tuple(random.randint(1, TAMANHO_MATRIZ) for _ in range (2))
        
        if (posicao_valida(matrix, pos) and not posicao_formiga(matrix, pos)):
            dx, dy = pos
            matrix[dx][dy] = 'o'
            setCorpos.add(pos)

# Função para movimentar as formigas
def movimentar_formigas(matrix, listaFormigas, setCorpos, visao):
    for formiga in listaFormigas:
        fx, fy = formiga.pos
        
        # A formiga escolhe uma direção e calcula a nova posição
        dx, dy = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
        nova_pos = (fx + dx, fy + dy)

        # Se a nova posição for inválida (fora da matriz), a formiga não faz nada nesta iteração (Pula para a próxima formiga).
        if (not posicao_valida(matrix, nova_pos)):
            continue

        # Possibilidade da formiga largar o corpo se estiver carregando
        if (formiga.carregando):
            
            formiga.pos = nova_pos
            if (formiga.pos not in setCorpos and largar_item(matrix, formiga.pos, visao)):
                formiga.carregando = False
                setCorpos.add(formiga.pos)

        # Possibilidade da formiga pegar um corpo
        else:
            
            # A formiga está em cima de um corpo
            if (nova_pos in setCorpos):
                if (pegar_item(matrix, nova_pos, visao)):
                    formiga.pos = nova_pos
                    formiga.carregando = True
                    setCorpos.remove(nova_pos)
                    
            # A formiga não está em cima de um corpo e apenas se move
            else:
                formiga.pos = nova_pos
    
    # Redesenha a matriz
    for i in range(1, TAMANHO_MATRIZ + 1):
        for j in range(1, TAMANHO_MATRIZ + 1):
            matrix[i][j] = ' '
            
    # Desenha primeiro todos os corpos que estão no chão
    for pos_corpo in setCorpos:
        cx, cy = pos_corpo
        matrix[cx][cy] = 'o'
    
    # Desenha as formigas em suas posições finais
    for formiga in listaFormigas:
        fx, fy = formiga.pos
        if (formiga.carregando):
            matrix[fx][fy] = '@'
        else:
            matrix[fx][fy] = 'X'
            
# Função main para rodar o código
def main():
    quadrados_visao = (2 * RAIO + 1)**2 - 1
    listaFormigas = []
    setCorpos = set()
    iteracoes = 0
    
    matriz = montar_matriz(TAMANHO_MATRIZ)
    inserir_formigas_corpos(matriz, listaFormigas, setCorpos)
    
    while True:
        print(f"Iteração: {iteracoes + 1}\nFormigas: {len(listaFormigas)}       Tamanho Matriz: {TAMANHO_MATRIZ}\nCorpos: {len(setCorpos)}        Raio: {RAIO}")
        mostrar_matriz(matriz)
        movimentar_formigas(matriz, listaFormigas, setCorpos, quadrados_visao)
        print()
        iteracoes += 1
        time.sleep(0.1)

if __name__ == "__main__":
	main()            
 
#Iteração: 1        
#Formigas: 10       Tamanho Matriz: 25
#Corpos: 150        Raio: 1
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#     o         o   o             o o o       o     #
#       o     o     o o         o       o     X   o #
#               o   o   o     o     o o o o o       #
#               o   o   o           o   o o   o     #
#       o o   X     o       o         X       o   o #
#   o       o                             o       o #
#               o   o               X o             #
#                     o     o o o                   #
# o   o o             o       o   o                 #
#             o   o   o o o o             o o       #
#     o     o o o         o     o             o     #
# o         o     o           o X               o   #
#                   o                 o     o       #
#     o o     o     o o X       X       o   o       #
# o   o o         o       o     o     o           X #
#   o   o               o             o o           #
#       o               o o   o                 X   #
#             X               o     o   o     o o   #
#     o   o   o       o         o       o       o   #
#     o         o o     o         o       o         #
#   o           o o o       o               o   o   #
#             o       o o   o o               o     #
#     o                 o       o           o     o #
#         o   o   o       o   o   o         o     o #
#         o o           o     o o           o   o   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # 



#Iteração: 1        
#Formigas: 10       Tamanho Matriz: 25
#Corpos: 150        Raio: 1
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#  o  o         o   o             o o o       o     #
#       o     o              o       o        o     #
#    @               o                              #
#            o   o   o   o           o   o o   o    #
#       o o        o       o            @   o   o   #
#   o     o                             o         o #
#    o o o         o   o        o o o o         o   #
#                     o     o o o                   #
# o   o o         @    o       o   o    o o o       #
#             o   o                         o o     #
#     o     o o o         o     o             o     #
# o   @      o     o   @        o        @        o #
#       @            o                 o     o      #
#     o o     o     o o         @       o   o       #
# o   o o         o       o     o     o             #
#   o   o               o             o o           #
#       o    o o o                 o o o o o        #
#                            o     o   o     o o    #
#     o   o   o       o         o       o       o   #
#     o         o o     o         o       o         #
#   o                  o               o   o        #
#             o       o o   o o               o     #
#     o             @    o       o           o    o #
#    @     o   o   o       o   o   o        o     o #
#         o o           o     o o           o   o   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # 


 
#Iteração: 5065        
#Formigas: 10          Tamanho Matriz: 25
#Corpos: 140           Raio: 1
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#   o o                        o       o o o        #
# o o o                     o o o     o o o         #
#                        o o o o                    #
#            o               o o               o    #
#                                o o o              #
#           o o o o                o o o o          #
#      o o  o o o                  o o o            #
#       o o o o                     o o             #
#        o o                o                       #
#   o            o           o o            o o o o #
# o o                       o o        o o o o o o  #
# o o                                   o o o o o o #
# o o                                    o o o o o  #
#                                                   #
#         o o               o                       #
#       o o o             o o         o o o         #
#       o o o             o o       o o o o o       #
#      o o o                       o o o o o        #
#      o o o o           o             o o o o o    #
#      o o o          o               o o o o o     #
#               o                     o o o o       #
#                        o o                        #
#   o          o     o o o o o                      #
#                         o o              o        #
#     o                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # #




















# Iteração: 1
# Formigas: 10       Tamanho Matriz: 25
# Corpos: 150        Raio: 1
# # # # # # # # # # # # # # # # # # # # # # # # # # #
# o o   o       X           o   o o       X       o #
#       o       o o               o                 #
#       o   o         o                 o o     o   #
#     o o o         o   o   o             o         #
# o         o       o   o               o           #
# o o             o   o     o         o       o     #
#     o           o             o     o           o #
#             o     o   o o     o           o   o o #
#       o   o o       o       o   o     o           #
#                           o     o     o o     o o #
#     o     o o             o     o o o       o     #
#     o o       o       o                   o X     #
#                       o   o   o           o   o   #
#       o o     o o     X o       X   o       o     #
#                 o   o                             #
#   o     o       o o   o o           X             #
#   o       o   o                           o   o   #
#   o X o   X                   o             o   o #
# o           o   o         o o     o               #
#   o   o     o   o       o         o         o     #
#                         o   o o     o o         o #
#               o o o       o               o o     #
#     o o     o           o           o       o     #
#   o   X o           o         o   o   o           #
# X o   o o   o                       o     o o   o #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

# Iteração: 2500
# Formigas: 10       Tamanho Matriz: 25
# Corpos: 140        Raio: 1
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#     o o                   o     o               o #
#     o o o     o     @                           @ #
#     o o o             o               o           #
#     o o o           o o o               o         #
#           o         o o o                         #
# o o             o                                 #
#     o                       o o o o o       o o o #
#             o             o o o o @ o             #
#       o   o o           o o o o o o o             #
#           o o             o o o o o o             #
#     o       o       @       o o o o         o o   #
#                       o       o o     @     o o   #
#       o               o                     o o   #
#       o o     o o                   o             #
#   @           o o o                               #
#   o           o o     o                           #
#   o               @                       o       #
#   o                                         o   o #
# o             o o         o o                     #
#   o   o       o o       o o o o   o         o     #
#               o o       o o o o     o o         o #
#               @   o       o               o o     #
#     o o     o                     @         o     #
#     o o             o             o o o           #
#       o     o                       o     @ o   o #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

# Iteração: 5000
# Formigas: 10       Tamanho Matriz: 25
# Corpos: 140        Raio: 1
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#     o o                   o     o               o #
#     o o o     o                                   #
#     o o o             o               o           #
#     o o o           o o o               o       o #
#           o         o o o                     o   #
# o o             o                   o             #
#     o                       o o o o o       o o o #
#             o             o o o o o o             #
#       o   o o           o o o o o o o             #
#           o o             o o o o o o             #
#     o o     o               o o o o         o o   #
#                       o       o o           o o   #
#       o               o                     o o   #
#     o o o     o o                   o             #
#               o o o                               #
#   o           o o     o                           #
#   o                                       o       #
#   o                                         o   o #
# o             o o         o o                     #
#   o   o       o o       o o o o   o         o     #
#               o o       o o o o     o o         o #
#                   o       o o             o o     #
#     o o     o                               o     #
#     o o                           o o o           #
#     o o     o                       o     o o   o #
# # # # # # # # # # # # # # # # # # # # # # # # # # #