# Ant-Clustering
Ant Clustering Algorithm - Agrupamento Bioinspirado
Este repositório contém a implementação de um algoritmo de Inteligência de Enxame (Swarm Intelligence) inspirado no comportamento de formigas reais, que organizam corpos em colônias para manter o ambiente limpo.

📌 O Problema
O desafio consiste em organizar itens dispersos aleatoriamente em uma grade bidimensional (ambiente toroidal) em agrupamentos coesos (clusters), sem que as formigas tenham uma visão global do mapa ou conhecimento prévio da estrutura dos dados.

O projeto foi dividido em duas etapas principais:

1. Clusterização Homogênea (formiga_simples.py)
Nesta etapa, todos os itens são idênticos. As formigas tomam decisões de coleta e depósito baseando-se puramente na densidade local:

Coleta: Se uma formiga encontra um item em uma região vazia, a probabilidade de pegá-lo é alta.

Depósito: Se uma formiga carregando um item encontra uma região com muitos outros itens, a probabilidade de soltá-lo é alta.

2. Clusterização Heterogênea (formiga_complexo.py)
Aqui, o problema evolui para a organização de dados complexos. Cada item possui características únicas (vetores de valores e pesos). A lógica de densidade é substituída pela Similaridade Local:

Distância Euclidiana: As formigas calculam o quão diferente um item é em relação aos seus vizinhos.

Raio Variável: Se a vizinhança imediata estiver muito vazia, a formiga expande seu campo de visão para tomar uma decisão mais robusta.

Atributos: O algoritmo é capaz de separar até 15 grupos distintos de dados, agrupando-os por afinidade estatística.

🛠️ Ferramentas
Python 3

NumPy (para geração de distribuições normais)

Matplotlib/Terminal (para visualização dos snapshots)


