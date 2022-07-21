from random import choice, choices, randrange
from time import time
import pandas as pd


def Instanciando(indexPath):
    with open("./Docs/" + PATH[indexPath] + ".txt", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split()
        for j in range(len(lines[i])):
            lines[i][j] = float(lines[i][j])
    return lines



def createPheromone(nCidades):
    data = []
    for i in range(nCidades):
        data.append([])
        for j in range(nCidades):
            data[i].append(nCidades)

    return data


def BCCF(pTable, tInitial, tLimit, dTable, nCidades):

    bestQuality = -1

    while time() - tInitial < tLimit:

        atualCity = randrange(nCidades)

        solution = [atualCity]

        localCities = [i for i in range(nCidades) if i != atualCity]
        probabilities = [0 for i in range(nCidades) if i != atualCity]

        while len(solution) != nCidades:

            for i in range(len(localCities)):

                pheromone = pTable[atualCity][localCities[i]]
                distance = dTable[atualCity][localCities[i]]

                probabilities[i] = pheromone / (distance * distance)

            # check if all probabilities are 0 (choices bugs when all are 0)
            if not sum(probabilities):
                chosen = choice(localCities)

            else:
                chosen = choices(
                    localCities, weights=probabilities, k=1)[0]

            solution.append(chosen)

            index = localCities.index(chosen)
            localCities.pop(index)
            probabilities.pop(index)

            atualCity = chosen

        #quality = qualityOfSolution(solution, dTable)
        quality = 0
        for i in range(len(solution) - 1):
            quality += dTable[solution[i]][solution[i+1]]

        quality += dTable[solution[-1]][solution[0]]

        # update pheromone table
        alpha = 0.8
        if quality < bestQuality or bestQuality == -1:
            bestQuality = quality
            alpha = 1.2

        # update pheromone table
        for i in range(len(solution) - 1):
            pTable[solution[i]][solution[i+1]] *= alpha
            pTable[solution[i+1]][solution[i]] *= alpha

        pTable[solution[-1]][solution[0]] *= alpha
        pTable[solution[0]][solution[-1]] *= alpha

    return bestQuality, tInitial



PATH = ["Djibouti", "Qatar", "Uruguay", "Western Sahara", "Zimbabwe"]
q_media , desvio , times = [],[],[]  

for i in range(len(PATH)):

    distanceTable = Instanciando(i)
    nCidades = len(distanceTable)
    tLimit = 60* nCidades /1000
    qualities , localTime = [],[]

    for j in range(1,11):
       
        bestQuality, tInitial = BCCF(createPheromone(nCidades),time(), tLimit, distanceTable, nCidades)

        qualities.append(bestQuality)
        localTime.append(time() - tInitial)
        #print( "time:{:.1f}".format( _, localTime))
        print('iter', j)
    print('\n')
    # media da qualidade
    q_media.append(round(sum(qualities) / len(qualities)))

    # media do tempo de execucao
    avgTime = sum(localTime) / len(localTime)

    times.append(round(avgTime))

    variance = 0  # desvio padrao da qualidade
    for quality in qualities:
        variance += (quality - q_media[-1]) ** 2
    variance = variance / len(qualities)
    desvio.append(round(variance ** 0.5, 2))


headers = ["instancia", "autoria", "algoritmo","q-medio", "q-desvio", "t-medio"]
df = pd.DataFrame({"instancia": PATH, "autoria": "Rafaelle", "algoritmo": "BCCF", "q-medio": q_media, "q-desvio": desvio, "t-medio": times})
df.to_csv("./resultados.csv", header=headers, index=False)