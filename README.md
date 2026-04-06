# Problema do caixeiro viajante (TSP) - Simulated Annealing
Este repositório contém a implementação de um algoritmo de Simulated Annealing (Recozimento Simulado) para resolver o Problema do Caixeiro Viajante (Traveling Salesman Problem - TSP). O projeto foca em encontrar rotas otimizadas para diferentes instâncias de cidades, minimizando a distância total percorrida.

📌 O Problema
O Problema do Caixeiro Viajante é um desafio clássico de otimização onde o objetivo é encontrar a rota mais curta que visite um conjunto de cidades exatamente uma vez e retorne à cidade de origem. Por ser um problema NP-difícil, utilizamos uma meta-heurística para encontrar soluções aproximadas de alta qualidade.

🚀 A Solução: Simulated Annealing
O algoritmo é inspirado no processo metalúrgico de resfriamento controlado de metais. Ele permite "saltos" para soluções piores no início do processo (alta temperatura) para escapar de mínimos locais, convergindo gradualmente para uma solução otimizada conforme a temperatura diminui.

Diferenciais da Implementação:
Múltiplos Esquemas de Resfriamento (Cooling Schedules): O código explora diferentes funções para a queda da temperatura, incluindo modelos lineares, hiperbólicos e a função Sigmóide, que apresentou os melhores resultados em termos de convergência.

Operadores de Perturbação: Implementação de técnicas como a troca de pares e o 2-Opt para explorar a vizinhança das rotas.

Análise Estatística: O script gera automaticamente gráficos de convergência e boxplots (via Matplotlib) para comparar o desempenho de diferentes execuções (runs), garantindo rigor científico na análise dos resultados.

📊 Instâncias Testadas
O algoritmo foi validado utilizando instâncias padrão de mercado:

Cidades 51: Instância de 51 cidades (com ótimo conhecido).

Cidades 100: Instância de 100 cidades para testar a escalabilidade e estabilidade do resfriamento.

🛠️ Ferramentas
Python 3

NumPy: Manipulação de matrizes de distância.

Matplotlib: Visualização das rotas e análise estatística.

Mplcursors: Interatividade nos gráficos gerados.
