import random
import time
import pandas as pd

#PATH = ["Djibouti", "Qatar", "Uruguay", "Saara", "Zimbabwe"]

TIME_LIMIT = 60
CITY_LIMIT = 1000


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


# Calcula a regra de 3 para o tempo de execução da instância
def instanceTimeLimit(nCities):

    return TIME_LIMIT * nCities / CITY_LIMIT


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


def writeToFile(instancia, autoria, algoritmo, q_medio, q_desvio, t_medio):

    headers = ["instancia", "autoria", "algoritmo",
               "q-medio", "q-desvio", "t-medio"]

    df = pd.DataFrame({"instancia": instancia, "autoria": "Rafinha",
                       "algoritmo": algoritmo, "q-medio": q_medio,
                       "q-desvio": q_desvio, "t-medio": t_medio})

    df.to_csv("./resultados.csv", header=headers, index=False)


def main():
    PATH = ["Djibouti", "Western"]
    TIME_LIMIT = 60
    CITY_LIMIT = 1000

    averages = []  # array com a avg das melhores solucoes para cada instancia
    deviations = []  # array com o dp das melhores solucoes para cada instancia
    times = []  # array com o tempo de execução para cada instancia

    for i in range(len(PATH)):

        matrizDistancias = readInstance(i)
        nCidades = len(matrizDistancias)
        pontos = [x for x in range(nCidades)]

        timeLimit = instanceTimeLimit(nCidades)
        times.append(round(timeLimit * 10))

        bestSolution = -1
        solutions = []

        for _ in range(10):

            initialTime = time.time()

            while(time.time() - initialTime < timeLimit):

                solution = randomAlgorithm(pontos, matrizDistancias)
                if qualityOfSolution(solution, bestSolution):
                    bestSolution = solution

            solutions.append(bestSolution)

        averages.append(round(sum(solutions) / len(solutions)))

        variance = 0
        for solution in solutions:
            variance += (solution - averages[-1]) ** 2
        variance = variance / len(solutions)
        deviations.append(round(variance ** 0.5, 2))

    writeToFile(PATH, "Fernando", "BTA", averages, deviations, times)


#CODIGO PRINCIPAL, chamando as função
if __name__ == '__main__':
	main()
