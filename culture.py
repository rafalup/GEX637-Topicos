import random
import time
import pandas as pd

# retorna a matriz de adjacencia da cidade em PATH[indexPath]
def readInstance(indexPath):
    PATH = ["Djibouti", "Western"]
    with open("Docs/" + PATH[indexPath] + ".txt", "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].split()
        for j in range(len(lines[i])):
            lines[i][j] = float(lines[i][j])
    return lines


def randomAlgorithm(pontos, matrizDistancias):

    random.shuffle(pontos)
    totalDistance = 0
    for i in range(len(pontos) - 1):
        totalDistance += matrizDistancias[pontos[i]][pontos[i+1]]

    # retorna para o primeiro ponto
    totalDistance += matrizDistancias[pontos[-1]][pontos[0]]
    return totalDistance


def qualityOfSolution(solution, bestSolution):
    if bestSolution == -1 or solution < bestSolution:
        return True
    return False




PATH = ["Djibouti", "Western"]

averages = []  # array com a avg das melhores solucoes para cada instancia
deviations = []  # array com o dp das melhores solucoes para cada instancia
times = []  # array com o tempo de execução para cada instancia

for i in range(len(PATH)):

    matrizDistancias = readInstance(i)
    nCidades = len(matrizDistancias)
    pontos = [x for x in range(nCidades)]

    timeLimit = 60 * nCidades / 1000 # Calcula a regra de 3 para o tempo de execução da instância
    times.append(round(timeLimit * 10))

    bestSolution = -1
    solutions = []

    while (i < 10):
        #for i in range(10):

        initialTime = time.time()

        while(time.time() - initialTime < timeLimit):

            solution = randomAlgorithm(pontos, matrizDistancias)
            if qualityOfSolution(solution, bestSolution):
                bestSolution = solution

        solutions.append(bestSolution)
            
        i+=1

    averages.append(round(sum(solutions) / len(solutions)))

    variance = 0
    for solution in solutions:
        variance += (solution - averages[-1]) ** 2
    variance = variance / len(solutions)
    deviations.append(round(variance ** 0.5, 2))

headers = ["instancia", "autoria", "algoritmo","q-medio", "q-desvio", "t-medio"]
df = pd.DataFrame({"instancia": PATH, "autoria": "Rafinha", "algoritmo": "BTA BOSTINHA", "q-medio": averages,"q-desvio": deviations, "t-medio": times})
df.to_csv("resultados.csv", header=headers, index=False)
