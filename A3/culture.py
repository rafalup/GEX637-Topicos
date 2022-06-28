import random
from time import time
import pandas as pd
from statistics import pstdev

def Instancia(indexPath):
    PATH = ["Djibouti", "Qatar", "Uruguay", "Western Sahara", "Zimbabwe"]
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
    #for i in range(len(solution) - 1):
    while(i < len(solution) -1):
        totalDistance += matrizDistancias[solution[i]][solution[i+1]]

    totalDistance += matrizDistancias[solution[-1]][solution[0]]
    return totalDistance



def tabuSearch(tInitial, tLimit, matrizDistancias, nCidades):

    mandato = nCidades // 5
    mandatoValues = [0 for _ in range(nCidades)]

    tabuList = []

    pivot = [x for x in range(nCidades)]
    random.shuffle(pivot)

   # bestQuality = qualityOfSolution(pivot, matrizDistancias)
    bestQuality = 0
    for i in range(len(pivot) - 1):
        bestQuality += matrizDistancias[pivot[i]][pivot[i+1]]

    bestQuality += matrizDistancias[pivot[-1]][pivot[0]]
  

    size = len(pivot)

    x = 0

    while (x < size) and (time() - tInitial < tLimit):

        if mandatoValues[pivot[x]] != 0:
            x += 1
            continue

        nextQuality = -1
        nextSolution = -1
        nextToTabu = []

        y = x + 2  # Comeca a partir de x + 2, para evitar 2opt com adjacente;
        while (y < size) and (time() - tInitial < tLimit):

            if (mandatoValues[pivot[y]] != 0):
                y += 1
                continue

            newSolution = swap(pivot, x, y)
            newQuality = qualityOfSolution(newSolution, matrizDistancias)
            # newQuality=0
            # for i in range(len(pivot) - 1):
            #    newQuality += matrizDistancias[pivot[i]][pivot[i+1]]
            # newQuality += matrizDistancias[pivot[-1]][pivot[0]]

            if (newQuality < nextQuality) or (nextQuality == -1):
                nextQuality = newQuality
                nextSolution = newSolution
                nextToTabu = (pivot[x], pivot[y])
                print("entrou aqui")

            y += 1

        pivot = nextSolution

        # Atualiza a melhor qualidade
        if nextQuality < bestQuality:
            bestQuality = nextQuality

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

    return bestQuality, tInitial

def tempo_medio(values_times):
    hora = 0
    for up in values_times: 
        hora += up

    hora = hora / len(values_times)
    times.append(round(hora))
    return times
    

#=============================  main principal ==================================
PATH = ["Djibouti", "Qatar", "Uruguay", "Western Sahara", "Zimbabwe"]
medio , desvio , times = [] ,[],[] 

for i in range(len(PATH)):
    matrizDistancias = Instancia(i)
    nCidades = len(matrizDistancias)
    tLimit = 60 * nCidades / 1000
    qualities , localTime = [], []

    for _ in range(10):

        bestQuality, tInitial = tabuSearch(
            time(), tLimit, matrizDistancias, nCidades)

        qualities.append(bestQuality)
        localTime.append(time() - tInitial)

      
    medio.append(round(sum(qualities) / len(qualities)))

    time_final = tempo_medio(localTime) #t_medio

    desvio.append(round(pstdev(qualities),1))

headers = ["instancia", "autoria", "algoritmo","q-medio", "q-desvio", "t-medio"]
df = pd.DataFrame({"instancia": PATH, "autoria": "Rafaelle", "algoritmo": "BT2opt", "q-medio": medio,
                       "q-desvio": desvio, "t-medio": time_final})
df.to_csv("./resultados.csv", header=headers, index=False)