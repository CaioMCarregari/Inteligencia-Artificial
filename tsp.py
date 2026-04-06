##############################################
#         INTELIGÊNCIA ARTIFICIAL    		 #
# Tarefa 2 - Problema do caixeiro viajante   #
# ALUNOS: Caio Marquiafave Carregari         #
#		  Clidenor Barbosa de Melo Neto      # 
##############################################

# Bibliotecas importadas
import random
import math
import sys
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import mplcursors
from matplotlib.patches import Patch

# Configurações globais
RUNS = 10
T0 = 2000
ITMAX = 500000
TEX = 3
TN = 0.001

# Função para carregar as instâncias de um arquivo de cidades (em formato txt)
def carregar_instancia(caminho_arquivo):
    cidades = []
    
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            partes = linha.split()
            
            id_cidade = int(partes[0])
            x = int(partes[1])
            y = int(partes[2])

            cidades.append([id_cidade, (x, y)])
    return cidades

# Função para calcular a matriz de distâncias das cidades
def calcular_matriz_distancias(cidades):
    n = len(cidades)
    # Primeiro, preenche todas as linhas da matriz com 0.0
    matriz = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            x1, y1 = cidades[i][1]
            x2, y2 = cidades[j][1]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            matriz[i][j] = matriz[j][i] = dist  # Simétrico
    
    return matriz

# Função para encontrar o vizinho mais próximo
def encontrar_vizinho_mais_proximo(cidade_atual, matriz, visitados): 
    vizinhos = []

    for i in range(len(matriz)):
        if i == cidade_atual or i in visitados:
            continue
        
        vizinhos.append((matriz[cidade_atual][i], i))
    
    menor_dist, cidade_mais_proxima = min(vizinhos)

    return cidade_mais_proxima, menor_dist

# Função para caminhar por todas as cidades
def caminhar_por_cidades(cidade_inicial, matriz):
    visitados = [cidade_inicial]  
    dist_total = 0
    
    cidade_atual = cidade_inicial

    while len(visitados) < len(matriz):
        vizinho, dist = encontrar_vizinho_mais_proximo(cidade_atual, matriz, visitados)
        visitados.append(vizinho)
        dist_total += dist
        cidade_atual = vizinho  # Atualiza posição atual
    
    # Volta à cidade inicial para fechar o ciclo do TSP
    dist_total += matriz[cidade_atual][cidade_inicial]
    visitados.append(cidade_inicial)

    return visitados

# Função para adicionar perturbação no caminho original
def perturbar_caminho(caminho):
    """
    Aplica uma das várias estratégias de perturbação:
    1. Swap aleatório de duas cidades
    2. Reversão de um subtrecho (2-opt)
    3. Inserção (move uma cidade de posição)
    4. Shuffle parcial (embaralha pequeno trecho)
    """
    caminho_perturbado = caminho.copy()
    n = len(caminho_perturbado)
    
    tipo = random.choice(["swap", "reversao", "insercao", "shuffle"])
    
    if tipo == "swap":
        # Troca simples de duas cidades
        i, j = random.sample(range(1, n - 1), 2)
        caminho_perturbado[i], caminho_perturbado[j] = caminho_perturbado[j], caminho_perturbado[i]
    
    elif tipo == "reversao":
        # Reversão (2-opt)
        i, j = sorted(random.sample(range(1, n - 1), 2))
        caminho_perturbado[i:j] = reversed(caminho_perturbado[i:j])
    
    elif tipo == "insercao":
        # Remove uma cidade e insere em outra posição
        i, j = random.sample(range(1, n - 1), 2)
        cidade = caminho_perturbado.pop(i)
        caminho_perturbado.insert(j, cidade)
    
    elif tipo == "shuffle":
        # Embaralha um trecho pequeno
        i, j = sorted(random.sample(range(1, n - 1), 2))
        trecho = caminho_perturbado[i:j]
        random.shuffle(trecho)
        caminho_perturbado[i:j] = trecho

    return caminho_perturbado

def calcular_temperatura(qual_formula, i):
    # Primeira fórmula - Professor
    if qual_formula == 1:
        return T0 * ((1 - i/ITMAX)**TEX)
    
    # Segunda fórmula - Hiperbólica
    elif qual_formula == 2:
        frac = i / ITMAX
        return (T0 - TN) / (1 + 30 * frac) + TN
    
    # Terceira fórmula - Sigmoid
    elif qual_formula == 3:
        return (T0 - TN) / (1 + math.exp(0.00003 * (i - ITMAX/2))) + TN
    
    # Quarta fórmula - Linear
    else:
        return T0 - i*((T0 - TN) / ITMAX) 
        
 
# Função main para executar o código
def main():
    print(f"======= Informações =======\nTemperatura inicial: {T0}\nMáximo iterações: {ITMAX}\nTN escolhido: {TN}\n")
    decide_instancia = int(input("Digite qual base de dados você quer carregar\n1 - 51 cidades\n2 - 100 cidades\n"))
    
    if decide_instancia == 1:
        cidades = carregar_instancia("cidades51.txt")

    else:
        cidades = carregar_instancia("cidades100.txt")
    
    if not cidades:
        print("Houve um erro no carregamento de dados!\n")
        sys.exit(0)
    
    decide_formula = int(input("\nDigite qual fórmula da temperatura deseja escolher \n1 - Fórmula do professor\n2 - Hiperbólica\n3 - Sigmoid\n4 - Linear\n"))
              
    matriz_distancias = calcular_matriz_distancias(cidades)
    resultados = []
    
    for run in range(RUNS):
        numero_inicial = random.randint(1, len(cidades))
        
        # Primeiro loop para saber a cidade de onde vai começar
        for i, cidade in enumerate(cidades):
            if cidade[0] == numero_inicial:
                primeira_cidade = i
                break 
        
        visitados = caminhar_por_cidades(primeira_cidade, matriz_distancias) 
        visitados_perturbados_inicial = perturbar_caminho(visitados)
        melhor_distancia = 0.0
        
        for i in range(len(visitados_perturbados_inicial) - 1):
                    a = visitados_perturbados_inicial[i] - 1
                    b = visitados_perturbados_inicial[i + 1] - 1
                    melhor_distancia += matriz_distancias[a][b]
                    
        distancia_inicial = melhor_distancia
        
        # Variáveis para realizar SA
        T = T0
        it = 0
        iter = []
        dist_atual = [] 
        melhor_dist = []
        temp_t = []
        
        while it < ITMAX:
            it += 1
            visitados_perturbados = perturbar_caminho(visitados)
            nova_distancia = 0
            
            for i in range(len(visitados_perturbados) - 1):
                a = visitados_perturbados[i] - 1
                b = visitados_perturbados[i + 1] - 1
                nova_distancia += matriz_distancias[a][b]
                
            delta = nova_distancia - distancia_inicial
            
            if delta < 0:
                visitados = visitados_perturbados
                distancia_inicial = nova_distancia
                if nova_distancia < melhor_distancia:
                    melhor_distancia = nova_distancia
            else:
                x = random.random()
                if x < math.exp(-delta / T):
                    visitados = visitados_perturbados
                    distancia_inicial = nova_distancia
                    
            iter.append(it)
            dist_atual.append(distancia_inicial)
            melhor_dist.append(melhor_distancia)
            temp_t.append(T)
        
            T = calcular_temperatura(decide_formula, it)
            
        resultados.append({
            "run": run + 1,
            "melhor_distancia": melhor_distancia,
            "iter": iter,
            "dist_atual": dist_atual,
            "melhor_dist": melhor_dist,
            "temp_t": temp_t
        })
        
        print(f"RUN {run + 1} finalizada. Melhor distância = {melhor_distancia:.2f}")
    
    # === Escolher o melhor resultado === #
    melhor_run = min(resultados, key=lambda r: r["melhor_distancia"])
    
    print("\n======= RESULTADO FINAL =======")
    print(f"Melhor RUN: {melhor_run['run']}")
    print(f"Melhor distância obtida: {melhor_run['melhor_distancia']:.2f}\n")
    
    # === PLOTAR GRÁFICO DA MELHOR RUN === #
    fig = plt.figure(figsize=(18, 5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2.5, 1])
    
    ax1 = plt.subplot(gs[0])
    linha1, = ax1.plot(melhor_run["iter"], melhor_run["dist_atual"], label='Distância', color='green')
    #linha2, = ax1.plot(melhor_run["iter"], melhor_run["melhor_dist"], label='Melhor Distância', color='blue')
    idx_best = np.argmin(melhor_run["melhor_dist"])
    ax1.scatter(melhor_run["iter"][idx_best], melhor_run["melhor_dist"][idx_best],
            s=50, c='red', label=f"Melhor: {melhor_run['melhor_distancia']:.2f}")
    ax1.set_title(f"Distância x Iterações (Melhor RUN #{melhor_run['run']})")
    ax1.set_xlabel("Iterações")
    ax1.set_ylabel("Distância total")
    ax1.grid(True)
    ax1.legend(fancybox=True, shadow=True)
    
    ax2 = plt.subplot(gs[1])
    linha3, = ax2.plot(melhor_run["iter"], melhor_run["temp_t"], label='Temperatura', color='red')
    temp_final = melhor_run["temp_t"][-1]
    ax2.scatter(melhor_run["iter"][-1], temp_final, s=50, c='black', edgecolor='yellow', zorder=5,
            label=f"T final = {temp_final:.2f}")
    ax2.set_title("Temperatura x Iterações")
    ax2.set_xlabel("Iterações")
    ax2.set_ylabel("Temperatura")
    ax2.grid(True)
    ax2.legend(fancybox=True, shadow=True)
    
    plt.suptitle(f"Melhor execução (RUN {melhor_run['run']}) - TSP com {len(cidades)} cidades")
    plt.tight_layout()
    
    # === CURSORES INTERATIVOS === #
    cursor1 = mplcursors.cursor([linha1, linha3], hover=True)
    @cursor1.connect("add")
    def on_hover(sel):
        x, y = sel.target
        sel.annotation.set_text(f"Iteração: {int(x)}\nValor: {y:.2f}")
        sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)
    
    plt.show()
    
    # Salvar gráfico da melhor RUN
    fig.savefig(f"melhor_RUN_{melhor_run['run']}_dist_{melhor_run['melhor_distancia']:.2f}.png", dpi=300)
    print(f"Gráfico salvo como 'melhor_RUN_{melhor_run['run']}_dist_{melhor_run['melhor_distancia']:.2f}.png'")

    # === ANÁLISE ESTATÍSTICA DAS RUNS === #
    distancias_finais = [r["melhor_distancia"] for r in resultados]
    media_final = np.mean(distancias_finais)
    desvio_final = np.std(distancias_finais)
    
    print("\n======= ANÁLISE ESTATÍSTICA =======")
    print(f"Média das melhores distâncias: {media_final:.2f}")
    print(f"Desvio padrão: {desvio_final:.2f}\n")
    
    # === PLOTAR GRÁFICO DE ANÁLISE === #
    fig2, ax = plt.subplots(1, 2, figsize=(14, 5))
    
    # Boxplot das distâncias
    box = ax[0].boxplot(distancias_finais, vert=True, patch_artist=True,
                    boxprops=dict(facecolor='lightblue'),
                    medianprops=dict(color='orange', linewidth=2),
                    whiskerprops=dict(color='gray'),
                    capprops=dict(color='gray'))

    ax[0].set_title("Distribuição das Melhores Distâncias (Boxplot)")
    ax[0].set_ylabel("Distância total")
    ax[0].grid(True)

    # Calcular estatísticas do boxplot
    q1 = np.percentile(distancias_finais, 25)
    q2 = np.percentile(distancias_finais, 50)  # mediana
    q3 = np.percentile(distancias_finais, 75)
    iqr = q3 - q1
    min_val = np.min(distancias_finais)
    max_val = np.max(distancias_finais)

    # Criar legenda explicativa
    legend_elements_box = [
        Patch(facecolor='lightblue', edgecolor='black', label=f"Q1 = {q1:.2f}"),
        Patch(facecolor='lightblue', edgecolor='black', label=f"Q3 = {q3:.2f}"),
        Patch(facecolor='orange', edgecolor='black', label=f"Mediana (Q2) = {q2:.2f}"),
        Patch(facecolor='none', edgecolor='gray', label=f"Intervalo: {min_val:.2f} – {max_val:.2f}")
    ]

    ax[0].legend(handles=legend_elements_box, fancybox=True, shadow=True, loc='upper right')
    
    # Gráfico de barras com média e desvio padrão
    runs = list(range(1, RUNS + 1))
    melhor_idx = np.argmin(distancias_finais)
    pior_idx = np.argmax(distancias_finais)
    desvio_pop = np.std(distancias_finais, ddof=0)  # populacional
    desvio_amostral = np.std(distancias_finais, ddof=1) 

    colors = []
    for i in range(len(distancias_finais)):
        if i == melhor_idx:
            colors.append('green')   # melhor
        elif i == pior_idx:
            colors.append('red')     # pior
        else:
            colors.append('skyblue') # demais

    bars = ax[1].bar(runs, distancias_finais, color=colors, edgecolor='black')
    ax[1].axhline(media_final, color='red', linestyle='--', label=f"Média = {media_final:.2f}")
    
    # Desvio padrão populacional
    ax[1].axhline(media_final + desvio_pop, color='orange', linestyle=':', linewidth=1.2)
    ax[1].axhline(media_final - desvio_pop, color='orange', linestyle=':', linewidth=1.2)
    
    # Desvio padrão amostral
    ax[1].axhline(media_final + desvio_amostral, color='darkorange', linestyle='-.', linewidth=1.2)
    ax[1].axhline(media_final - desvio_amostral, color='darkorange', linestyle='-.', linewidth=1.2)
    
    ax[1].fill_between(runs, media_final - desvio_final, media_final + desvio_final,
                       color='orange', alpha=0.2, label=f"Desvio ±{desvio_final:.2f}")
    ax[1].set_title("Melhores distâncias por RUN")
    ax[1].set_xlabel("RUN")
    ax[1].set_ylabel("Melhor distância")
    
    elementos_legenda = [
    Patch(facecolor='green', edgecolor='black', label=f"Melhor RUN ({runs[melhor_idx]}) = {distancias_finais[melhor_idx]:.2f}"),
    Patch(facecolor='red', edgecolor='black', label=f"Pior RUN ({runs[pior_idx]}) = {distancias_finais[pior_idx]:.2f}"),
    Patch(facecolor='none', edgecolor='red', linestyle='--', label=f"Média = {media_final:.2f}"),
    Patch(facecolor='none', edgecolor='orange', linestyle=':', label=f"σ (Populacional) = {desvio_pop:.2f}"),
    Patch(facecolor='none', edgecolor='darkorange', linestyle='-.', label=f"s (Amostral) = {desvio_amostral:.2f}")
    ]
    
    ax[1].legend(handles=elementos_legenda, fancybox=True, shadow=True)
    ax[1].grid(True)
    
    plt.suptitle("Análise Estatística das RUNS - Simulated Annealing (TSP)")
    plt.tight_layout()
    
    # === CURSORES INTERATIVOS NOS GRÁFICOS ESTATÍSTICOS === #
    cursor2 = mplcursors.cursor(bars, hover=True)
    @cursor2.connect("add")
    def on_hover_bar(sel):
        idx = int(sel.index)
        sel.annotation.set_text(f"RUN {runs[idx]}\nDistância: {distancias_finais[idx]:.2f}")
        sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)
    
    cursor3 = mplcursors.cursor(box['boxes'], hover=True)
    @cursor3.connect("add")
    def on_hover_box(sel):
        sel.annotation.set_text("Boxplot das distâncias")
        sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)
    
    plt.show()
    
    # Salvar figura estatística
    fig2.savefig(f"analise_estatistica_runs_dist_{melhor_run['melhor_distancia']:.2f}.png", dpi=300)
    print(f"Gráfico estatístico salvo como 'analise_estatistica_runs_dist{melhor_run['melhor_distancia']:.2f}.png'")
    
if __name__ == "__main__":
	main()