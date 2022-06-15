import random
import time
import pandas as pd
from statistics import pstdev

# retorna a matriz de adjacencia da cidade em PATH[indexPath]
def Instanciando(indexPath):
    PATH = ["Djibouti", "Qatar","Uruguay","Western Sahara","Zimbabwe"]
    with open("Docs/" + PATH[indexPath] + ".txt", "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].split()
        for j in range(len(lines[i])):
            lines[i][j] = float(lines[i][j])
    return lines


def algoritmoAleatorio(pontos, matrizDistancias):

    random.shuffle(pontos)
    totalDistance = 0
    for i in range(len(pontos) - 1):
        totalDistance += matrizDistancias[pontos[i]][pontos[i+1]]

    # retorna para o primeiro ponto
    totalDistance += matrizDistancias[pontos[-1]][pontos[0]]
    return totalDistance



PATH = ["Djibouti", "Qatar","Uruguay","Western Sahara","Zimbabwe"]
media, desviopadrao, times,  solutions = [],[],[],[]

for i in range(len(PATH)):

    matrizDistancias = Instanciando(i)
    nCidades = len(matrizDistancias)
    pontos = [x for x in range(nCidades)]

    timeLimit = 60 * nCidades / 1000 
    times.append(round(timeLimit * 10))

    bestSolution = -1
    culture = []
    while (i < 10):
       
        initialTime = time.time()

        while(time.time() - initialTime < timeLimit):

            solution = algoritmoAleatorio(pontos, matrizDistancias)
            
            if bestSolution == -1 or solution < bestSolution:
                print(solution)
                culture.append(solution)
                bestSolution = solution


        solutions.append(bestSolution)
            
        i+=1

    media.append(round(sum(solutions) / len(solutions)))

    
    desviopadrao.append(round(pstdev(culture),1))

headers = ["instancia", "autoria", "algoritmo","q-medio", "q-desvio", "t-medio"]
df = pd.DataFrame({"instancia": PATH, "autoria": "Rafaelle", "algoritmo": "BTA", "q-medio": media,"q-desvio": desviopadrao, "t-medio": times})
df.to_csv("resultados.csv", header=headers, index=False)
