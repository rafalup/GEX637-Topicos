import random
from time import time
import pandas as pd
from statistics import pstdev

def Instanciando(indexPath):
    PATH = ["Djibouti", "Qatar","Uruguay","Western Sahara","Zimbabwe"]
    with open("Docs/" + PATH[indexPath] + ".txt", "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].split()
        for j in range(len(lines[i])):
            lines[i][j] = float(lines[i][j])
    return lines


def swap(arr, a, b):
    x = arr[a:b]
    A = arr[:a]
    B = arr[b:]
    x.reverse()
    A.extend(x)
    A.extend(B)

    return A

def qualityOfSolution(solution, matrizDistancias):

    totalDistance = 0
    for i in range(len(solution) - 1):
        totalDistance += matrizDistancias[solution[i]][solution[i+1]]

    totalDistance += matrizDistancias[solution[-1]][solution[0]]
    return totalDistance


def tabuSearch(tInitial, tLimit, matrizDistancias, nCidades, culture):
    tabuList = []
    bestQuality = 0
    x = 0

    mandato = nCidades // 5
    mandatoValues = [0 for _ in range(nCidades)]

    pivot = [n for n in range(nCidades)]
    random.shuffle(pivot)

    
    for i in range(len(pivot) - 1):
        bestQuality  += matrizDistancias[pivot[i]][pivot[i+1]]

    bestQuality  += matrizDistancias[pivot[-1]][pivot[0]]
    
    size = len(pivot)

    while (x < size) and (time() - tInitial < tLimit):

        if mandatoValues[pivot[x]] != 0:
            x += 1
            continue

        nextQuality = -1
        nextSolution = -1
        nextToTabu = ()

        y = x + 2  
        while (y < size) and (time() - tInitial < tLimit):

            if (mandatoValues[pivot[y]] != 0):
                y += 1
                continue

            newSolution = swap(pivot, x, y)
            newQuality = qualityOfSolution(newSolution, matrizDistancias)

            if (newQuality < nextQuality) or (nextQuality == -1):
                nextQuality = newQuality
                nextSolution = newSolution
                nextToTabu = (pivot[x], pivot[y])

            y += 1

        pivot = nextSolution

        # Atualiza a melhor qualidade
        if nextQuality < bestQuality:
            bestQuality = nextQuality
            print(bestQuality)
           
        # Atualiza a lista tabu
        newTabuList = []
        for i in tabuList:
            mandatoValues[i] -= 1
            if mandatoValues[i] != 0:
                newTabuList.append(i)
        tabuList = newTabuList

        # Adiciona x e y para a lista tabu
        for i in nextToTabu:
            tabuList.append(i)
            mandatoValues[tabuList[-1]] = mandato

        x = 0
    culture.append(bestQuality)

    return bestQuality, tInitial


# ===================    main principal         ===================
PATH = ["Djibouti", "Qatar", "Uruguay", "Western Sahara", "Zimbabwe"]
averages , deviations , culture, times = [], [], [], []

for i in range(len(PATH)):

    matrizDistancias = Instanciando(i)
    nCidades = len(matrizDistancias)
        
    tLimit = (60 * nCidades) / 1000
    times.append(round(tLimit))

    qualities, localTime = [] , []

    for _ in range(10):

        bestQuality, tInitial = tabuSearch(
            time(), tLimit, matrizDistancias, nCidades,culture)

        qualities.append(bestQuality)
        localTime.append(time() - tInitial)

    averages.append(round(sum(qualities) / len(qualities)))
    
    deviations.append(round(pstdev(culture),1))

headers = ["instancia", "autoria", "algoritmo","q-medio", "q-desvio", "t-medio"]
df = pd.DataFrame({"instancia": PATH, "autoria": "Rafaelle", "algoritmo": "BTA", "q-medio": averages,"q-desvio": deviations, "t-medio": times})
df.to_csv("resultados.csv", header=headers, index=False)